#!/usr/local/bin/python3

import json
import boto3
import decimal

session = boto3.Session(profile_name='dev')
ddb = session.resource('dynamodb', region_name='eu-west-1')

table = ddb.Table('Components')

class Component:
    def __init__(self, name, responsible_team):
        self.name = name
        self.responsible_team = responsible_team
        self.repo_link = "set the repo links"
        self.description = "update me"

    def dump(self):
        print("[ \n\tComponent:\t" + str(self.name) + "\n\tResponsible:\t" + str(self.responsible_team) + "\n\tRepo Link:\t" +
              str(self.repo_link) + "\n\tDescription\t" + str(self.description) + " \n]")

    def update_description(self, description):
        self.description = description
        self.save()

    def update_repolink(self, repo_link):
        self.repo_link = repo_link
        self.save()

    def save(self):
        response = table.put_item(
            Item={
                'name': self.name,
                'responsible_team': self.responsible_team,
                'repo_link': self.repo_link,
                'description': self.description
            }
        )
        # print(json.dumps(response, indent=4))

# # populate procedure
components_mng = {}
response = table.scan()
# print(response)
components = response['Items']
for component in components:
    components_mng[component['name']] = Component(component['name'], component['responsible_team'])
    components_mng[component['name']].update_description(component['description'])
    components_mng[component['name']].update_repolink(component['repo_link'])

# components_mng['jenkins'] = Component('Jenkins', 'Ops')
print(components_mng)
