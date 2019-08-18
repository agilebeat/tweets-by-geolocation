import boto3
import random
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from configparser import ConfigParser
from decimal import Decimal
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as Vader


def load_credentials_from_config_file(cfg_file):
    parser = ConfigParser()
    parser.read(cfg_file)
    access_token = parser.get('api_tracker', 'access_token')
    access_token_secret = parser.get('api_tracker', 'access_token_secret')
    consumer_key = parser.get('api_tracker', 'consumer_key')
    consumer_secret = parser.get('api_tracker', 'consumer_secret')
    return consumer_key, consumer_secret, access_token, access_token_secret


class Listener(StreamListener):
    def __init__(self, api=None):
        super(StreamListener, self).__init__()
        self.table = self.__get_maprover_table('tweets-by-location')
        self.num_tweets = 0

    def __get_maprover_table(self, table_name):
        DynaDB = boto3.resource('dynamodb')
        maproverTable = DynaDB.Table(table_name)
        return maproverTable

    def __compute_sentiment(self, tweet):
        sid = Vader()
        sent_score = sid.polarity_scores(tweet)
        sent_status = None

        if sent_score['pos'] > 0 and sent_score['compound'] > 0:
            sent_status = 'positive'
        elif sent_score['neg'] > 0 and sent_score['compound'] < 0:
            sent_status = 'negative'
        else:
            sent_status = 'neutral'
        sent_score = sent_score['compound']
        return sent_status, sent_score

    def __compute_point_location(self, all_data):
        longitude = None
        latitude = None
        rnd_longitude = None
        rnd_latitude = None
        true_loc = False
        coordinates = all_data.get('coordinates', None)
        if coordinates is not None:
            coor = coordinates.get('coordinates', [longitude, latitude])
            longitude = coor[0]
            rnd_longitude = longitude
            latitude = coor[1]
            rnd_latitude = latitude
            true_loc = True
        else:
            coor = all_data['place']['bounding_box']['coordinates'][0]
            longitude = (coor[0][0] + coor[3][0]) / 2
            rnd_longitude = coor[0][0] + random.uniform(0, 1) * (coor[3][0]-coor[0][0])
            latitude = (coor[0][1] + coor[1][1]) / 2
            rnd_latitude = coor[0][1] + random.uniform(0, 1) * (coor[1][1]-coor[0][1])
        return longitude, latitude, rnd_longitude, rnd_latitude, true_loc


    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        sent_status, sent_score = self.__compute_sentiment(tweet)
        longitude, latitude, rnd_longitude, rnd_latitude, is_true_loc = self.__compute_point_location(all_data)

        TweetInfo = {
            'UserID': all_data["id_str"],
            'Created_Time': all_data["created_at"],
            'Text': tweet,
            'Longitude': longitude,
            'Latitude': latitude,
            'RndLongitude': rnd_longitude,
            'RndLatitude': rnd_latitude,
            'Sent_Score': sent_score,
            'Sent_Status': sent_status,
            'TrueLoc': is_true_loc
        }

        TweetInfo = json.dumps(TweetInfo)
        TweetInfo = json.loads(TweetInfo, parse_float=Decimal)
        self.table.put_item(Item=TweetInfo)
        self.num_tweets = self.num_tweets + 1
        if self.num_tweets % 10 == 0:
            print ("processed: " + str(self.num_tweets))
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    #long_lat = [174.1747029878635, -37.38018420811879, 175.96585269347128, -36.350780565204055]
    long_lat = [166.509144322, -46.641235447, 178.517093541, -34.4506617165] # New Zeland
    track_words = ['train', 'train station', 'railroad', 'commuter', 'railway station', 'railroad station', 'railroad terminal', 'train station', 'train depot']
    consumer_key, consumer_secret, access_token, access_token_secret = load_credentials_from_config_file('api_auth.cfg')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterStream = twitterStream = Stream(auth, Listener())
    twitterStream.filter(locations=long_lat)
