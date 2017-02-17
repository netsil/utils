import click
import json
import requests
from requests import session
from aocurls import *
from alert_template import template
from cliutils import PrettyPrint

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
        PrettyPrint(parsed, ["id", "name", "alertTemplateId", "serviceId"])
        return


def GetAlertDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertURL = GetAlertDetailsURL()
        alertURL = alertURL + "/" + id
        response = c.get(alertURL)
        parsed = json.loads(response.text)
 
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


#== CLI Commands ==
@click.command()
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (id, name, template id, service id); > 1 (all)')
def list(verbose):
    '''List all alerts '''
    GetAlertList(verbose)


@click.command()
@click.option('-k','--key', multiple=True, help='List of attributes to print. Print all if an attribute is not found')
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






