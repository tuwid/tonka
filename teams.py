#!/bin/python

import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

session = boto3.Session(profile_name='dev')
ddb = session.resource('dynamodb', region_name='eu-west-1')

# For a Boto3 service resource ('resource' is for higher-level, abstracted access to Dynamo)
# ddb = boto3.resource(
#     'dynamodb',
#     aws_access_key_id="anything",
#     aws_secret_access_key="anythoing",

# )

table = ddb.Table('Teams')

class Team:
    def __init__(self, name, tech_lead):
        self.name = name
        self.tech_lead = tech_lead
        self.members = []
        self.slack_rooms = []

    def dump(self):
        print("[ \n\t" + str(self.name) + "\n\t" + self.tech_lead + "\n\t" +
              str(self.members) + "\n\t" + str(self.slack_rooms) + + " ] \n")

    def add_member(self, member):
        self.members.append(member)
        # self.members = list(dict.fromkeys(self.members))
        self.save()
    
    def remove_member(self, member):
        print(type(self.members))
        self.members.remove(member)
        self.save()

    def add_slackroom(self, slackroom):
        self.slack_rooms.append(str(slackroom))
        # self.slack_rooms = list(dict.fromkeys(self.slack_rooms))
        self.save()

    def remove_slackroom(self, slackroom):
        print(type(self.slack_rooms))
        self.slack_rooms.remove(slackroom)
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




# # populate procedure
teams_mng = {}
response = table.scan()
teams = response['Items']
for team in teams:
    teams_mng[team['name']] = Team(team['name'], team['tech_lead'])
    for member in team['members']:
        teams_mng[team['name']].add_member(member)
    for slack in team['slack_rooms']:
        teams_mng[team['name']].add_slackroom(slack)
    teams_mng[team['name']].save()
    print(team)

# teams = []
# teams.append(Team("Ops", "Milos"))
# teams['Ops'].add_member('Artur D')
# teams['Ops'].add_member('Milos R')
# teams['Ops'].add_slackroom('#dev-ops')
# teams['Ops'].add_slackroom('#team-infrastructure')
# teams['Ops'].remove_member('#team-infrastructure')
# teams_mng['Reliability'].add_member('Javier M')
# teams_mng['Reliability'].add_member('Jose G')
# teams_mng['Reliability'].add_slackroom('#team-reliability')   
# teams_mng['Reliability'].remove_member('#team-reliability')  
teams_mng['Reliability'].dump()
