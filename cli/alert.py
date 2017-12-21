import click
import json
import requests
from requests import session
from aocurls import *
from alert_template import template
from alert_rule import rule
from alert_policy import policy
from cliutils import PrettyPrint
from qparser import QueryStringParser
from analytics import CreateQuery
from analytics import CreateQueriesFromStringList

#== Command Execution Functions ==

def GetAlertList(verbose):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertURL())
        parsed = json.loads(response.text)
        if verbose > 1:
            print json.dumps(parsed, indent=4, sort_keys=True)
            return;
        alertCount = 0
        PrettyPrint(parsed, ["id", "name"])
        return


def GetAlertDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertURL = GetAlertDetailsURL()
        alertURL = alertURL + "/" + id
        response = c.get(alertURL)
        parsed = json.loads(response.text)
 
        if len(keys) == 0:
            print json.dumps(parsed, indent=4, sort_keys=True)
            return

        for key in keys:
            if key in parsed.keys():
                print key + ": \t " + json.dumps(parsed[key], indent=4, sort_keys=True)
            else:
                print json.dumps(parsed, indent=4, sort_keys=True)
                return
        return


def DeleteAlert(id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertURL = GetAlertDetailsURL()
        alertURL = alertURL + "/" + id
        response = c.delete(alertURL)
        return  



def CreateAlertNotification(alertId, policyType, policyId):
    alertNotify = {}
    alertNotify["alertId"] = alertId
    alertNotify["policyId"] = policyId
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertNotificationURL = GetAlertNotificationURL(policyType)
        print alertNotify
        response = c.post(alertNotificationURL, json=alertNotify)
        parsed = json.loads(response.text)
        print json.dumps(parsed, indent=4, sort_keys=True)
        return parsed 




def CreateAlert(critical, warning, operator, duration, aggregation, plot, policy_type, policy_id, name, query):
    queries = []
    queries.append(query)
    alert = {}
    alert["name"]=name
    tmpQueries = CreateQueriesFromStringList(queries, True)
    alert["queries"]=tmpQueries["queries"]
    qNames = tmpQueries["queryNames"]
    alert["selectedReferences"]=[]
    alert["selectedReferences"].append(qNames[0])
    alert["filters"]=[]
    
    plotType = plot + "-chart"
    alert["chartTypes"]={ "main query" : plotType }

    alert["description"]=query

    agg = { "function" : aggregation, "duration" : duration * 60 }
    comp = { "operator" : operator, "criticalThreshold": critical, "warningThreshold": warning }
    alert["conditions"] = { "aggregation" : agg, "comparison" : comp }

    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertCreateURL = GetAlertCreateURL()
        response = c.post(alertCreateURL, json=alert)
        parsed = json.loads(response.text)
        print json.dumps(parsed, indent=4, sort_keys=True)
        if policy_id != None and policy_type != None:
            alertNotification = CreateAlertNotification(parsed["id"], policy_type, policy_id)
        return parsed 

    




#== CLI Commands ==
@click.command()
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (id, name, template id, service id); > 1 (all)')
def list(verbose):
    '''List all alerts '''
    GetAlertList(verbose)


@click.command()
@click.option('-k','--key', multiple=True, help='List of attributes to print. Print all if an attribute is not found')
@click.argument('alert_id')
def get(key, alert_id):
    '''Details for alert '''
    GetAlertDetails(key, alert_id)


@click.command()
@click.argument('alert_id')
def delete(alert_id):
    ''' Delete Alert '''
    if click.confirm("Do you want to delete the alert?"):
        DeleteAlert(alert_id)

@click.command()
@click.option('-c', '--critical', type=float, help='Critical threshold')
@click.option('-w', '--warning', type=float, help='Warning threshold')
@click.option('-o', '--operator', type=click.Choice(['>','<','=']), default='>', help='Operator to check for threshold violation e.g. > critical threshold')
@click.option('-d', '--duration', type=click.Choice(['1','5','10','30','60']), default='1', help='Time window to evaluate the alert, in mins')
@click.option('-a', '--aggregation', type=click.Choice(['avg', 'max', 'min']), default='avg', help='Aggregation function to apply for metrics in time window')
@click.option('-p', '--plot', type=click.Choice(['line','area','stack-bar','bar', 'table', 'pie', 'gauge']), default='line', help='Chart plot type')
@click.option('-t', '--policy_type', type=click.Choice(['webhook','email','pagerduty']), help='Notification policy type. Check out alert policy list for more details')
@click.option('-i', '--policy_id', help='Notification policy id. Check out alert policy list for more details')
@click.argument('name')
@click.argument('query')
def create(critical, warning, operator, duration, aggregation, plot, policy_type, policy_id, name, query):
    ''' Create Alert '''
    # hack to get around a bug in click.types during display help
    duration = int(duration)
    if isinstance(policy_id, unicode):
        policy_id= policy_id.encode('utf-8')
    CreateAlert(critical, warning, operator, duration, aggregation, plot, policy_type, policy_id, name, query)




#== CLI Command Group ==
@click.group()
def alert():
    ''' Netsil AOC Alert Commands '''
    pass

alert.add_command(template)
alert.add_command(rule)
alert.add_command(policy)
alert.add_command(list)
alert.add_command(get)
alert.add_command(delete)
alert.add_command(create)






