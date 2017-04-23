import click
import json
import requests
from requests import session
from aocurls import *
from cliutils import PrettyPrint, JSONLoadsString
from qreader import QueryReader
from botutils import *     

#== Command Execution Functions ==

def GetAlertRuleList(formatOutput="formatted"):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertRuleURL())
        parsed = json.loads(response.text)

        if(formatOutput=="text"):
            return PrettyResponseText(parsed, ["id", "alertTemplateId", "name", "description"])
        elif(formatOutput=="raw"):
            return json.dumps(parsed, indent=4, sort_keys=True)
        else:
            return PrettyResponseTable(parsed, ["id", "alertTemplateId", "name", "description"], "Alert Rule List")



def GetAlertRuleDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertRuleURL = GetAlertRuleDetailsURL()
        alertRuleURL = alertRuleURL + "/" + id
        response = c.get(alertRuleURL)
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

def GetQueryList(id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertRuleURL = GetAlertRuleDetailsURL()
        alertRuleURL = alertRuleURL + "/" + id
        response = c.get(alertRuleURL)
        parsed = JSONLoadsString(response.text)
        queries = parsed["queries"]
        
        for query in queries:
           queryDetails = QueryReader(query)
           if "queries" in queryDetails.keys():
               return PrettyPrint(queryDetails["queries"])
           if "expressions" in queryDetails.keys():
               return PrettyPrint(queryDetails["expressions"])

def DeleteAlertRule(id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertRuleURL = GetAlertRuleDetailsURL()
        alertRuleURL = alertRuleURL + "/" + id
        response = c.delete(alertRuleURL)
        return








