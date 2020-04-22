#!/usr/local/bin/python3
import json
import boto3


# For a Boto3 service resource ('resource' is for higher-level, abstracted access to Dynamo)
ddb = boto3.resource(
    'dynamodb', 
    aws_access_key_id="anything", 
    aws_secret_access_key="anythoing",
    endpoint_url='http://localhost:8000', 
    region_name='eu-west-1'
)

#Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def create_table(table_name):
    # filter + error handling 
    params = {
        'TableName': table_name,
        'KeySchema': [
            {'AttributeName': "name", 'KeyType': "HASH"},    # Partition key
            {'AttributeName': "tech_lead", 'KeyType': "RANGE"}
        ],
        'AttributeDefinitions': [
            {'AttributeName': "name", 'AttributeType': "S"},
            {'AttributeName': "tech_lead", 'AttributeType': "S"},
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    }
    ddb.create_table(**params)
    return()


if( len(list(ddb.tables.all())) > 0):
    print('Tables already there')
    print(list(ddb.tables.all()))
else:
    print('Creating tables')
    create_table('Teams')
    create_table('Components')

# ddb.create_table(**params)
