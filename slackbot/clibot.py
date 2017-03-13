import os
import time
from slackclient import SlackClient
import json
import requests
from requests import session
from aocurls import *
from cliutils import *

#-------------------ALERTS------------------------------------------

def GetAlertList(formatOutput="formatted"):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertURL())
        parsed = json.loads(response.text)
        if(formatOutput=="text"):
            return PrettyResponse(parsed, ["id", "name", "alertTemplateId", "serviceId"])
        elif(formatOutput=="raw"):
            return json.dumps(parsed, indent=4, sort_keys=True)
        else:
            return PrettyResponseColored(parsed, ["id", "name", "alertTemplateId", "serviceId"], "Alert List")


def GetAlertDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertURL = GetAlertDetailsURL()
        alertURL = alertURL + "/" + id
        response = c.get(alertURL)
        parsed = json.loads(response.text)
        response=''

        if len(keys) == 0:
            response += json.dumps(parsed, indent=4, sort_keys=True)
            return response


        for key in keys:
            if key in parsed.keys():
                response += key + ": \t " + json.dumps(parsed[key], indent=4, sort_keys=True)
            else:
                response += json.dumps(parsed, indent=4, sort_keys=True)
                
        return response      

#-------------------SERVICE-------------------------------------------

def GetServiceList(formatOutput="formatted"):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetServiceURL())
        parsed = json.loads(response.text)
        
        if(formatOutput=="text"):
            return PrettyResponse(parsed, ["serviceId", "name", "description"])
        elif(formatOutput=="raw"):
            return json.dumps(parsed, indent=4, sort_keys=True)
        else:
            return PrettyResponseColored(parsed, ["serviceId", "name", "description"], "Service List")

        
        

def GetServiceDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        serviceURL = GetServiceDetailsURL()
        serviceURL = serviceURL + "/" + id
        response = c.get(serviceURL)
        parsed = json.loads(response.text)
        response=''

        if len(keys) == 0:
            response += json.dumps(parsed, indent=4, sort_keys=True)
            return response

       
        for key in keys:
            if key in parsed.keys():
                response += key + ": \t " + json.dumps(parsed[key], indent=4, sort_keys=True)
            else:
                response += json.dumps(parsed, indent=4, sort_keys=True)
                
        return response

#-------------------CLI BOT-------------------------------------------

BOT_NAME = 'cli'
SLACK_BOT_TOKEN = 'xoxb-153327665858-NaTzgNgsLeK3FUv4ylHsiTZC'

# starterbot's ID as an environment variable
#BOT_ID = os.environ.get("BOT_ID")
BOT_ID='U4H9MKKR8'

# constants
AT_BOT = "<@" + BOT_ID + ">"
COMMANDS=['alert', 'service']

#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient(SLACK_BOT_TOKEN)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + str(COMMANDS) + \
               "* command with numbers, delimited by spaces."
    if command.startswith(COMMANDS[0]):
        #print command
        if(command.split(' ')[1]=='list'):
            if(len(command.split(' '))>2):
                formatOutput = command.split(' ')[2]
            else:
                formatOutput=''

            response = GetAlertList(formatOutput)

            if(formatOutput=='' or formatOutput == 'formatted'):
                slack_client.api_call("chat.postMessage", channel=channel,
                          attachments=response, as_user=True)
            else:
                slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

        if(command.split(' ')[1]=='details'):
            response = GetAlertDetails([],command.split(' ')[2])
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

    if command.startswith(COMMANDS[1]):
        if(command.split(' ')[1]=='list'):
            if(len(command.split(' '))>2):
                formatOutput = command.split(' ')[2]
            else:
                formatOutput=''

            response = GetServiceList(formatOutput)

            if(formatOutput=='' or formatOutput == 'formatted'):
                slack_client.api_call("chat.postMessage", channel=channel,
                          attachments=response, as_user=True)
            else:
                slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

        if(command.split(' ')[1]=='details'):
            response = GetServiceDetails([],command.split(' ')[2])
            slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

    #print response
    #slack_client.api_call("chat.postMessage", channel=channel,
    #                      text=response, as_user=True)
    #slack_client.api_call("chat.postMessage", channel=channel,
    #                      attachments=response, as_user=True)


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


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("CLIBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
