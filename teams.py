#!/usr/local/bin/python3

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
        self.po = "-"
        self.members = []
        self.slack_rooms = []

    def dump(self):
        print("[ \n\tTeam Name:\t" + str(self.name) + "\n\tTeach Lead:\t" + str(self.tech_lead) + "\n\tProduct Owner:\t" + str(self.po) + "\n\tMembers:\t" +
              str(self.members) + "\n\tSlackRooms\t" + str(self.slack_rooms) + " \n]")
        return("[ \n\tTeam Name:\t" + str(self.name) + "\n\tTeach Lead:\t" + str(self.tech_lead) + "\n\tProduct Owner:\t" + str(self.po) + "\n\tMembers:\t" +
              str(self.members) + "\n\tSlackRooms\t" + str(self.slack_rooms) + " \n]")

    def add_member(self, member):
        self.members.append(member)
        self.members = list(dict.fromkeys(self.members))
        self.save()
    
    def remove_member(self, member):
        self.members.remove(member)
        self.save()

    def add_slackroom(self, slackroom):
        self.slack_rooms.append(str(slackroom))
        self.slack_rooms = list(dict.fromkeys(self.slack_rooms))
        self.save()

    def remove_slackroom(self, slackroom):
        self.slack_rooms.remove(slackroom)
        self.save()

    def update_lead(self, t_lead):
        self.tech_lead = t_lead
        self.save()

    def update_po(self, po):
        self.po = po
        self.save()
    
    def save(self):
        response = table.put_item(
            Item={
                'name': self.name,
                'tech_lead': self.tech_lead,
                'product_owner': self.po,
                'members': self.members,
                'slack_rooms': self.slack_rooms,
            }
        )
        # print(json.dumps(response, indent=4))


# class TeamsManager:
#     def __init__(self, name):
#         self.name = name
#         self.teams = []
#         self.teams_list = []

#     def add_team(self,t):
#         self.teams.append(t)
#         self.data

#     def dump(self):
#         print(self.name)

#     def get_data(self):
#         print(self.name)

def get_team_names(t_mng):
    names = []
    for t in t_mng:
        names.append(t)
        # print(t['name'], ' ', t['tech_lead'])
    return names

# # init "team manager"
teams_mng = {}
response = table.scan()
teams = response['Items']
for team in teams:
    teams_mng[team['name']] = Team(team['name'], team['tech_lead'])
    teams_mng[team['name']].update_po(team['product_owner'])
    for member in team['members']:
        teams_mng[team['name']].add_member(member)
    for slack in team['slack_rooms']:
        teams_mng[team['name']].add_slackroom(slack)
    teams_mng[team['name']].save()
    print(team)

# teams_mng['Ops'].add_member('Artur D')
# teams_mng['Ops'].add_slackroom('#dev-ops')
# teams_mng['Reliability'].add_member('Javier M')
# teams_mng['Reliability'].add_slackroom('#team-reliability')   
# teams_mng['Reliability'].dump()
# teams_mng['Ops'].dump()
