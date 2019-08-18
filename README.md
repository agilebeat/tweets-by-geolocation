# twitter-by-geolocation
Retrieve tweets based on geolocation information and save to AWS dynamoDB

## Notebook implementation

 Notebooks are in the notebook folder

### Create-DynamoDB-table.ipynb
Create Table on AWS DynamoDB 
UserID, Create_Time : Primary Key
Latitude, Longitude, Sent_Score (polarity score of tweets), Sent_Status (polarity, e.g. 'positive', 'negative' or 'neutral'), and Text

### twitter-given-lat-long.ipynb
Retrive tweets (streaming), analyzing tweets and send to DynamoDB

## Python implementation

### setup-dynamo-db-table.py

To set up dynamodb table:
- Make sure that you have boto3 installed.
- Make sure that your aws client is set up.
- Run it: ```setup-dynamo-db-table.py```


