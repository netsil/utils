import click
import json
import requests
from requests import session
from aocurls import *
from cliutils import PrettyPrint, JSONLoadsString
from qreader import QueryReader

#== Command Execution Functions ==

def GetAlertRuleList(verbose):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertRuleURL())
        parsed = json.loads(response.text)
        if verbose > 1:
            print json.dumps(parsed, indent=4, sort_keys=True)
            return;
        alertCount = 0
        PrettyPrint(parsed, ["id", "alertTemplateId", "name", "description"])
        return


def GetAlertDetails(keys, id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertRuleURL = GetAlertRuleDetailsURL()
        alertRuleURL = alertRuleURL + "/" + id
        response = c.get(alertRuleURL)
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
               PrettyPrint(queryDetails["queries"])
           if "expressions" in queryDetails.keys():
               PrettyPrint(queryDetails["expressions"])

        
        return



def DeleteAlertRule(id):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertRuleURL = GetAlertRuleDetailsURL()
        alertRuleURL = alertRuleURL + "/" + id
        response = c.delete(alertRuleURL)
        return


#== CLI Commands ==
@click.command()
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (id, name, template id, service id); > 1 (all)')
def list(verbose):
    '''List All Alert Rules'''
    GetAlertRuleList(verbose)


@click.command()
@click.option('-k','--key', multiple=True, help='List of attributes to print. Print all if an attribute is not found')
@click.argument('rule_id')
def details(key, rule_id):
    '''Details For Alert Rule'''
    GetAlertDetails(key, rule_id)


@click.command()
@click.argument('rule_id')
def delete(rule_id):
    ''' Delete Alert Rule'''
    if click.confirm("Do you want to delete the alert rule?"):
        DeleteAlertRule(rule_id)

@click.command()
@click.argument('rule_id')
def query(rule_id):
    ''' List All Queries '''
    GetQueryList(rule_id)



#== CLI Command Group ==
@click.group()
def rule():
    ''' Netsil AOC Alert Rule Commands'''
    pass

rule.add_command(list)
rule.add_command(details)
rule.add_command(delete)
rule.add_command(query)






