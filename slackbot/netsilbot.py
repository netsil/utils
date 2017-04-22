from service import *
from alert import *

import os
import time
from slackclient import SlackClient
import json
import requests
from requests import session
from aocurls import *
from botutils import *     
from alert_rule import *
from alert_template import *

BOT_NAME = GetBotName()
SLACK_BOT_TOKEN = GetBotToken()
slack_client = SlackClient(SLACK_BOT_TOKEN)
READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
COMMANDS=['alert', 'service'] #Slackbot commands

def GetBotID():
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')
    else:
        return

BOT_ID=GetBotID()
AT_BOT = "<@" + BOT_ID + ">"

def sendSlackMessage(msg, channel):
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=msg, as_user=True)

def sendSlackMessageWithAttactment(msg, channel):
    slack_client.api_call("chat.postMessage", channel=channel,
                          attachments=msg, as_user=True)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. " + \
                "Try the following commands: \n" +\
                "@netsilbot alert list\n" +\
                "@netsilbot alert details <alertID>\n" +\
                "@netsilbot service list\n" +\
                "@netsilbot service details <serviceID>\n"+\
                "(You can add 'text' or 'raw' options for formatting the output)"


    if command.startswith(COMMANDS[0]):
        #print command
        subcommand = command.split(' ')[1]
        if(subcommand=='list'):
            if(len(command.split(' '))>2):
                formatOutput = command.split(' ')[2]
            else:
                formatOutput=''

            response = GetAlertList(formatOutput)

            if(formatOutput=='' or formatOutput == 'formatted'):
                sendSlackMessageWithAttactment(response, channel)
            else:
                sendSlackMessage(response, channel)

        elif(subcommand=='details'):
            response = GetAlertDetails([],command.split(' ')[2])
            sendSlackMessage(response, channel)

        elif(subcommand=='rule'):
            subsubcommand = command.split(' ')[2]
            if(subsubcommand=='list'):
                if(len(command.split(' '))>3):
                    formatOutput = command.split(' ')[3]
                else:
                    formatOutput=''

                response = GetAlertRuleList(formatOutput)
                
                if(formatOutput=='' or formatOutput == 'formatted'):
                    sendSlackMessageWithAttactment(response, channel)
                else:
                    sendSlackMessage(response, channel)

            elif(subsubcommand=='details'):
                response = GetAlertRuleDetails([],command.split(' ')[3])
                sendSlackMessage(response, channel)
            else:
                sendSlackMessage(response, channel)

        elif(subcommand=='template'):
            subsubcommand = command.split(' ')[2]
            if(subsubcommand=='list'):
                if(len(command.split(' '))>3):
                    formatOutput = command.split(' ')[3]
                else:
                    formatOutput=''

                response = GetAlertTemplateList(formatOutput)
                
                if(formatOutput=='' or formatOutput == 'formatted'):
                    sendSlackMessageWithAttactment(response, channel)
                else:
                    sendSlackMessage(response, channel)

            elif(subsubcommand=='details'):
                response = GetAlertTemplateDetails([],command.split(' ')[3])
                sendSlackMessage(response, channel)

            else:
                sendSlackMessage(response, channel)

    elif command.startswith(COMMANDS[1]):
        subcommand = command.split(' ')[1]
        if(subcommand=='list'):
            if(len(command.split(' '))>2):
                formatOutput = command.split(' ')[2]
            else:
                formatOutput=''

            response = GetServiceList(formatOutput)

            if(formatOutput=='' or formatOutput == 'formatted'):
                sendSlackMessageWithAttactment(response, channel)
            else:
                sendSlackMessage(response, channel)

        elif(subcommand=='details'):
            response = GetServiceDetails([],command.split(' ')[2])
            sendSlackMessage(response, channel)
        
        else:
            sendSlackMessage(response, channel)

    else:
        sendSlackMessage(response, channel)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def runbot():
    if slack_client.rtm_connect():
        print("Netsil SlackBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                try:
                    handle_command(command, channel)
                except:
                    slack_client.api_call("chat.postMessage", channel=channel,
                          text="Error in processing request", as_user=True)
                    pass
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")


if __name__ == "__main__":
	runbot()
