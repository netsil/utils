#import click
import json
import requests
from requests import session
from aocurls import *
#from cliutils import PrettyPrint
from botutils import *  

#== Command Execution Functions ==

def GetAlertTemplateList(formatOutput="formatted"):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertTemplateURL())
        parsed = json.loads(response.text)

        if(formatOutput=="text"):
            return PrettyResponseText(parsed, ["id","name"])
        elif(formatOutput=="raw"):
            return json.dumps(parsed, indent=4, sort_keys=True)
        else:
            return PrettyResponseTable(parsed, ["id","name"], "Alert Template List")


def GetAlertTemplateDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        templateURL = GetAlertTemplateDetailsURL()
        templateURL = templateURL + "/" + id
        response = c.get(templateURL)
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

	
