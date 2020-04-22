
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

table = ddb.Table('Components')

class Component:
    def __init__(self, id, name, responsible_team, repo_link):
        self.id = id
        self.name = name
        self.responsible_team = responsible_team
        self.repo_link = repo_link

    def dump(self):
        return("[ " + str(self.name) + " ] - " + self.responsible_team + " - " + str(self.repo_link))
    
    def save(self):
        # print(json.dumps(response, indent=4))


Components = []
Components.append(Component(0, "Jenkins", "Ops",'github..//'))
# print(Components[0].dump())

Components[0].save()

