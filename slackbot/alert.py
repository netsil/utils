import json
import requests
from requests import session
from aocurls import *
from botutils import *

#== Command Execution Functions ==
def GetAlertList(formatOutput="formatted"):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertURL())
        parsed = json.loads(response.text)
        if(formatOutput=="text"):
            return PrettyResponseText(parsed, ["id", "name", "alertTemplateId", "serviceId"])
        elif(formatOutput=="raw"):
            return json.dumps(parsed, indent=4, sort_keys=True)
        else:
            return PrettyResponseTable(parsed, ["id", "name", "alertTemplateId", "serviceId"], "Alert List")


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

def DeleteAlert(id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertURL = GetAlertDetailsURL()
        alertURL = alertURL + "/" + id
        response = c.delete(alertURL)
        return








