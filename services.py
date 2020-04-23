#!/usr/local/bin/python3

import json
import boto3
import decimal

session = boto3.Session(profile_name='dev')
ddb = session.resource('dynamodb', region_name='eu-west-1')

table = ddb.Table('Services')

class Service:
    def __init__(self, name, responsible_team):
        self.name = name
        self.responsible_team = responsible_team
        self.repo_link = "set the repo link"
        self.service_link = "ze service link"
        self.description = "update me"

    def dump(self):
        print("[ \n\tService:\t" + str(self.name) + "\n\tResponsible:\t" + str(self.responsible_team) + "\n\tRepo Link:\t" + 
              str(self.repo_link) + "\n\tService Link:\t" + str(self.service_link) + "\n\tDescription\t" + str(self.description) + " \n]")
        return("[ \n\tService:\t" + str(self.name) + "\n\tResponsible:\t" + str(self.responsible_team) + "\n\tRepo Link:\t" +
              str(self.repo_link) + "\n\tService Link:\t" + str(self.service_link) + "\n\tDescription\t" + str(self.description) + " \n]")

    def update_description(self, description):
        self.description = description
        self.save()

    def update_repolink(self, repo_link):
        self.repo_link = repo_link
        self.save()

    def update_servicelink(self, service_link):
        self.service_link = service_link
        self.save()

    def save(self):
        response = table.put_item(
            Item={
                'name': self.name,
                'responsible_team': self.responsible_team,
                'repo_link': self.repo_link,
                'service_link': self.service_link,
                'description': self.description
            }
        )
        # print(json.dumps(response, indent=4))

def get_service_names(services_mng):
    names = "*(micro)Service* - _Team Responsible_ \n _====================================\n"
    for t in services_mng:
        # print(services_mng[t].name)
        names += "- *" + t + "* - _" + str(services_mng[t].responsible_team) + "_ \n"
        # print(t['name'], ' ', t['tech_lead'])
    return names

# # populate procedure
services_mng = {}
response = table.scan()
services = response['Items']
# print(response)
for service in services:
    services_mng[service['name']] = Service(service['name'], service['responsible_team'])
    services_mng[service['name']].update_description(service['description'])
    services_mng[service['name']].update_repolink(service['repo_link'])
    # services_mng[service['name']].dump()
