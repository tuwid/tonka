
#!/bin/python

import json
import boto3
import decimal

# For a Boto3 service resource ('resource' is for higher-level, abstracted access to Dynamo)
ddb = boto3.resource(
    'dynamodb',
    aws_access_key_id="anything",
    aws_secret_access_key="anythoing",
    endpoint_url='http://localhost:8000',
    region_name='eu-west-1'
)

table = ddb.Table('Teams')

class Team:
    def __init__(self, id, name, tech_lead):
        self.id = id
        self.name = name
        self.tech_lead = tech_lead
        self.members = []
        self.slack_rooms = []

    def dump(self):
        return("[ " + str(self.name) + " ] - " + self.tech_lead + " - " + str(self.members) + " " + str(self.slack_rooms))

    def add_member(self, member):
        self.members.append(member)
        self.save()
    
    def remove_member(self, member):
        self.members.append(member)
        self.save()

    def add_slackroom(self, slackroom):
        self.members.append(member)
        self.save()
    
    def save(self):
        # some dynamo save logic
        # response = table.put_item(
        #     Item={
        #         'name': 'Ops',
        #         'tech_lead': 'Milos',
        #         'members': ['Doe','Jim','Milos'],
        #         'slack_rooms': ['#dev-ops', '#team-infrastructure'],
        #     }
        # )
        # response = table.get_item(
        #     Key={
        #         'name': 'Ops',
        #         'tech_lead': 'Milos'
        #     }
        # )
        # item = response['Item']
        # print(item)
        # response = table.update_item(
        #     Key={
        #         'name': 'Ops',
        #         'tech_lead': 'Milos'
        #     },
        #     UpdateExpression='SET age = :val1',
        #     ExpressionAttributeValues={
        #         ':val1': 26
        #     }
        # )
        # print(json.dumps(response, indent=4))


teams = []
teams.append(Team(0, "Ops", "Milos"))
# print(teams[0].dump())

teams[0].save()

