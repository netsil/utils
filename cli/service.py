import click
import json
import requests
from requests import session
from aocurls import *

#== Command Execution Functions ==

def GetServiceList(verbose):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetServiceURL())
        parsed = json.loads(response.text)
               
        if verbose > 1:
            print json.dumps(parsed, indent=4, sort_keys=True)
            return;
 
        # base verbosity: print id, name, description
        print ("Service Id \t,\t Service Name \t,\t Service Description") 
        print ("-------------------------------------------------------------------------------------------------------")
        for service in parsed:
            print (str(service["serviceId"]) + "\t,\t" + str(service["name"]) + " \t,\t" + str(service["description"]))
            
        print ("-------------------------------------------------------------------------------------------------------")
        print len(parsed)
        return

def GetServiceDetails(key, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        serviceURL = GetServiceDetailsURL()
        serviceURL = serviceURL + "/" + id
        response = c.get(serviceURL)
        parsed = json.loads(response.text)
        
        if key in parsed.keys():
            print json.dumps(parsed[key], indent=4, sort_keys=True)
            return
       
        
        print json.dumps(parsed, indent=4, sort_keys=True)
        return



#== CLI Commands ==

@click.command()
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (basic id,name,desc); > 1 (all)')
def list(verbose):
    '''List all services'''
    GetServiceList(verbose)


@click.command()
@click.option('-k','--key', help='Value of specific service attribute. print all if key not found')
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
	
