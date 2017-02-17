import click
import json
import requests
from requests import session
from aocurls import *
from cliutils import PrettyPrint

#== Command Execution Functions ==

def GetServiceList(verbose):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetServiceURL())
        parsed = json.loads(response.text)
               
        if verbose > 1:
            print json.dumps(parsed, indent=4, sort_keys=True)
            return;
        
        PrettyPrint(parsed, ["serviceId", "name", "description"])
        return

def GetServiceDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        serviceURL = GetServiceDetailsURL()
        serviceURL = serviceURL + "/" + id
        response = c.get(serviceURL)
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
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (basic id,name,desc); > 1 (all)')
def list(verbose):
    '''List all services'''
    GetServiceList(verbose)


@click.command()
@click.option('-k','--key', multiple=True, help='List of attributes to print. Print all if an attribute is not found')
@click.argument('service_id')
def details(key, service_id):
    '''Details for service'''
    GetServiceDetails(key, service_id)


#== CLI Command Group ==

@click.group()
def service():
    ''' Netsil AOC Service Commands '''
    pass

service.add_command(list)
service.add_command(details)
	
