import click
import json
import requests
from requests import session
from aocurls import *
from cliutils import PrettyPrint

#== Command Execution Functions ==

def GetAlertTemplateList(verbose):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertTemplateURL())
        parsed = json.loads(response.text)
               
        if verbose > 1:
            print json.dumps(parsed, indent=4, sort_keys=True)
            return;
 
        # base verbosity: print id, name, description
        for template in parsed:
            template["#instances"]=len(template["AlertInstances"])

        PrettyPrint(parsed, ["id","name","#instances"])
        return


def GetAlertTemplateDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        templateURL = GetAlertTemplateDetailsURL()
        templateURL = templateURL + "/" + id
        response = c.get(templateURL)
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


#== CLI Commands ==

@click.command()
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (id name, number of alerts using template); > 1 (all)')
def list(verbose):
    '''List all alert templates'''
    GetAlertTemplateList(verbose)


@click.command()
@click.option('-k','--key', multiple=True, help='List of attributes to print. Print all if an attribute is not found')
@click.argument('template_id')
def details(key, template_id):
    '''Details for alert template'''
    GetAlertTemplateDetails(key, template_id)


#== CLI Command Group ==

@click.group()
def template():
    ''' Commands for alert templates '''
    pass

template.add_command(list)
template.add_command(details)
	
