
#!/bin/python

import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr


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
    def __init__(self, name, tech_lead):
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
        self.members.append(slackroom)
        self.save()
    
    def save(self):
        # some dynamo save logic
        response = table.put_item(
            Item={
                'name': self.name,
                'tech_lead': self.tech_lead,
                'members': self.members,
                'slack_rooms': self.slack_rooms,
            }
        )
        # print(json.dumps(response, indent=4))


# # teams_list = []
# # teams.append(Team("Ops", "Milos"))
# # teams.append(Team("Reliability", "Javier"))
# # # print(teams[0].dump())

# # teams[0].save()
# # teams[1].save()

# # populate procedure
# teams_mng = {}
# response = table.scan()
# teams = response['Items']
# for team in teams:
#     teams_mng[team['name']] = Team(team['name'], team['tech_lead'])
#     for member in team['members']:
#         teams_mng[team['name']].add_member(member)
#     for slack in team['slack_rooms']:
#         teams_mng[team['name']].add_slackroom(slack)
#     teams_mng[team['name']].save()
#     print(team)


