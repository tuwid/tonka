
#!/bin/python

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
        self.repo_link = ""
        self.description = ""

    def dump(self):
        print("[ \n\Component:\t" + str(self.name) + "\n\Responsible:\t" + str(self.responsible_team) + "\n\Repo Link:\t" +
              str(self.repo_link) + "\n\Description\t" + str(self.description) + " \n]")

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
components = response['Items']
for component in components:
    components_mng[component['name']] = Component(component['name'], component['responsible_team'])
    components_mng[component['name']].update_description(component['description'])
    components_mng[component['name']].update_repolink(component['repo_link'])

# jenkins = Component('Jenkins','Ops')
# jenkins.save()