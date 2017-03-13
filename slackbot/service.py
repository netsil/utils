import json
import requests
from requests import session
from aocurls import *
from botutils import *

#== Command Execution Functions ==
def GetServiceList(formatOutput="formatted"):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetServiceURL())
        parsed = json.loads(response.text)
        
        if(formatOutput=="text"):
            return PrettyResponseText(parsed, ["serviceId", "name", "description"])
        elif(formatOutput=="raw"):
            return json.dumps(parsed, indent=4, sort_keys=True)
        else:
            return PrettyResponseTable(parsed, ["serviceId", "name", "description"], "Service List")


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
