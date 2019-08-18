import boto3

def set_up_table_in_dynamodb():    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='tweets-by-location',
        KeySchema=[{
                'AttributeName': 'UserID',
                'KeyType': 'HASH'
            }, {
                'AttributeName': 'Created_Time',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[{
                'AttributeName': 'UserID',
                'AttributeType': 'S'
        },{
                'AttributeName': 'Created_Time',
                'AttributeType': 'S'
        },],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    table.meta.client.get_waiter('table_exists').wait(TableName='tweets-by-location')
    print(table.item_count)

if __name__ == "__main__":
    set_up_table_in_dynamodb()