import click
import json
import requests
from requests import session
from aocurls import *
from alert_template import template



#== Command Execution Functions ==

def GetAlertList(verbose):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertTemplateURL())
        parsed = json.loads(response.text)
               
        if verbose > 1:
            for template in parsed:
                alertInstances = template["AlertInstances"]
                for alert in alertInstances:
                    print json.dumps(alertInstance, indent=4, sort_keys=True)
            return;
 
        # base verbosity: print id, name, template id, service id
        print ("Alert Id \t,\t Alert Name \t,\t Alert Template Id \t,\t Service Id") 
        print ("-------------------------------------------------------------------------------------------------------")
        alertCount = 0
        for template in parsed:
            alertInstances = template["AlertInstances"]
            for alert in alertInstances:
                print (str(alert["id"]) + "\t,\t" + str(alert["name"]) + " \t,\t" + str(alert["alertTemplateId"]) + "\t,\t" + str(alert["serviceId"]))
                alertCount = alertCount + 1 

        print ("-------------------------------------------------------------------------------------------------------")
        print alertCount
        return


def GetAlertDetails(key, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertURL = GetAlertDetailsURL()
        alertURL = alertURL + "/" + id
        response = c.get(alertURL)
        parsed = json.loads(response.text)
        
        if key in parsed.keys():
            print json.dumps(parsed[key], indent=4, sort_keys=True)
            return
            
        print json.dumps(parsed, indent=4, sort_keys=True)

        return

def DeleteAlert(id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertURL = GetAlertDetailsURL()
        alertURL = alertURL + "/" + id
        response = c.delete(alertURL)
        return


#== CLI Commands ==
@click.command()
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (id, name, template id, service id); > 1 (all)')
def list(verbose):
    '''List all alerts '''
    GetAlertList(verbose)


@click.command()
@click.option('-k','--key', help='Value of specific alert attribute. print all if key not found')
@click.argument('alert_id')
def details(key, alert_id):
    '''Details for alert '''
    GetAlertDetails(key, alert_id)


@click.command()
@click.argument('alert_id')
def delete(alert_id):
    ''' Delete Alert '''
    if click.confirm("Do you want to delete the alert?"):
        DeleteAlert(alert_id)


#== CLI Command Group ==
@click.group()
def alert():
    ''' Netsil AOC Alert Commands '''
    pass

alert.add_command(template)
alert.add_command(list)
alert.add_command(details)
alert.add_command(delete)






