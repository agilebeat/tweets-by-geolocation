# twitter-by-geolocation
Retrieve tweets based on geolocation information and save to AWS dynamoDB

## Create-DynamoDB-table.ipynb
Create Table on AWS DynamoDB 
UserID, Create_Time : Primary Key
Latitude, Longitude, Sent_Score (polarity score of tweets), Sent_Status (polarity, e.g. 'positive', 'negative' or 'neutral'), and Text

## twitter-given-lat-long.ipynb
Retrive tweets (streaming), analyzing tweets and send to DynamoDB


