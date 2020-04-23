#!/usr/local/bin/python3
import json
import boto3


import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

session = boto3.Session(profile_name='dev')
ddb = session.resource('dynamodb', region_name='eu-west-1')

#Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def create_table(table_name, attr):
    # filter + error handling 
    params = {
        'TableName': table_name,
        'KeySchema': [
            {'AttributeName': "name", 'KeyType': "HASH"},    # Partition key
            {'AttributeName': attr, 'KeyType': "RANGE"}
        ],
        'AttributeDefinitions': [
            {'AttributeName': "name", 'AttributeType': "S"},
            {'AttributeName': attr, 'AttributeType': "S"},
        ],
        'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    }
    ddb.create_table(**params)
    return()

# TODO: check if tables already exist

print('Creating tables')
# create_table('Teams', 'tech_lead')
create_table('Services', 'responsible_team')
