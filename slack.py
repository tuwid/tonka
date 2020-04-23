import os
import time
import re
import socket
from slackclient import SlackClient
from teams import *

slack_client = SlackClient(os.environ.get('SLACK_API_KEY'))
authorized_slack_channels = os.environ.get('AUTHORIZED_SLACK_CHANNELS')
authorized_users = os.environ.get('AUTHORIZED_USERS')


help_menu = """
This bot supports these cool things:
*!teams*                                  - list teams
*!teams add <team> <lead>*                - add new team ie !teams add rugby @Alaa.C
*!teams del <team>*                       - remove team ie !teams del Ops
*!teams add_member <team> <member>*         - add person to team ie !teams add_member Ops
*!teams del_member <team> <member>*         - add person to team ie !teams add_member Ops
*!teams add_room <team> <slack_room>*     - add slack room to team ie !teams add_slack Ops
*!teams del_room <team> <slack_room>*     - add slack room to team ie !teams add_slack Ops
*!teams list <team>*                      - list data on team ie !teams list Ops
*!services*                               - list services
*!pci*                                    - list PCI touching components
"""

if authorized_slack_channels:
    authorized_slack_channels = authorized_slack_channels.split(",")

# List of email addresses of the authorized users
authorized_users = os.environ.get('AUTHORIZED_USERS')
if authorized_users:
    authorized_users = authorized_users.split(",")

RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
starterbot_id = None
trigger_command = '!'

def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            # print(event)
            # user_id, message = parse_direct_mention(event["text"])
            # print(user_id, ' ', message)
            # if user_id == starterbot_id:
            #     return message, event["channel"]
            return event["text"], event["channel"], event["user"]
    return None, None, None


def send_command(slack_client, channel, text):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=text
    )


def handle_command(command, channel):
    default_response = "Not sure what you mean. Try *{}* help.".format(
        trigger_command)
    response = None

    # TODO: dont forget to lowercase everything!
    if command.startswith(trigger_command):
        command_array = command.split()
        if(command_array == ['!help']):
            response = help_menu
            send_command(slack_client, channel, response)
        if(command_array == ['!teams']):
            response = get_team_names(teams_mng)
            send_command(slack_client, channel, response)

        if(len(command_array) > 1):
            if(command_array[0] == '!team' or command_array[0] == '!teams'):
                if(command_array[1] in ['list', 'add', 'delete', 'set', 'add_member', 'add_room', 'del_member', 'del_room']):
                    if command_array[1] == 'add':
                            teams_mng[command_array[2]] = Team(command_array[2], command_array[3])
                            teams_mng[command_array[2]].save()
                            send_command(slack_client, channel, "Request sent to dynamo")
                    if command_array[1] == 'list':
                            response = teams_mng[command_array[2]].dump()
                            send_command(slack_client, channel, response)
                    if command_array[1] == 'add_member':
                            response = teams_mng[command_array[2]].add_member(command_array[3])
                            send_command(slack_client, channel, "Member added to team")
                    if command_array[1] == 'del_member':
                            response = teams_mng[command_array[2]].remove_member(
                                command_array[3])
                            send_command(slack_client, channel, "Member removed from team")
                    if command_array[1] == 'del_room':
                            response = teams_mng[command_array[2]].remove_slackroom(
                                command_array[3])
                            send_command(slack_client, channel, "Room removed from team")
                    if command_array[1] == 'add_room':
                            response = teams_mng[command_array[2]].add_slackroom(command_array[3])
                            send_command(slack_client, channel, "Slack room added to team")
        else:
            response = 'Invalid command layout, please ask Artur'
            send_command(slack_client, channel,response)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]

        while True:
            command, channel, user = parse_bot_commands(
                slack_client.rtm_read())
            if command:
                try:
                    channel_info = slack_client.api_call(
                        "channels.info", channel=channel)
                    channel_name = channel_info["channel"]["name"]
                    user_info = slack_client.api_call("users.info", user=user)
                    user_name = user_info["user"]["profile"]["email"]
                except Exception:
                    continue
                if authorized_slack_channels:
                    if channel_name not in authorized_slack_channels:
                        if command.startswith(trigger_command):
                            print("Received command from unauthorized slack channel {}, only commands from channels {} will be accepted".format(
                                channel_name, str(authorized_slack_channels)))
                            send_command(
                                slack_client, channel, "This Slack channel is not authorized to execute Arnold commands")
                        continue
                if authorized_users:
                    if user_name not in authorized_users:
                        if command.startswith(trigger_command):
                            print("Received command from unauthorized user {}, only commands from users {} will be accepted".format(
                                user_name, str(authorized_users)))
                            send_command(slack_client, channel, "{}, you are not authorized to execute {} command".format(
                                user_name, str(command)))
                        continue
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
