import click
import json
import requests
from requests import session
from aocurls import *
from cliutils import PrettyPrint

#== Command Execution Functions ==

def GetAlertWebhookPolicyList():
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertPolicyURL("webhook"))
        parsed = json.loads(response.text)
        PrettyPrint(parsed, ["id","name","uri"])
        return parsed

def GetAlertEmailPolicyList():
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertPolicyURL("email"))
        parsed = json.loads(response.text)
        PrettyPrint(parsed, ["id","email"])
        return parsed

def GetAlertPagerDutyPolicyList():
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetAlertPolicyURL("pagerduty"))
        parsed = json.loads(response.text)
        print json.dumps(parsed, indent=4, sort_keys=True)
        return parsed



def GetAlertPolicyList(policytype):
    if policytype == "webhook" or policytype == None:
        print "WebHook Alert Policies"
        GetAlertWebhookPolicyList()

    if policytype == "email" or policytype == None:
        print "Email Alert Policies"
        GetAlertEmailPolicyList()

    if policytype == "pagerduty" or policytype == None:
        print "PagerDuty Alert Policies"
        GetAlertPagerDutyPolicyList()
    
    return


def GetAlertPolicyDetails(id, ptype):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        policyURL = GetAlertPolicyURL(ptype)
        policyURL = policyURL + "/" + id
        response = c.get(policyURL)
        parsed = json.loads(response.text)
        print json.dumps(parsed, indent=4, sort_keys=True)
        return

def DeleteAlertPolicy(id, ptype):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        alertPolicyURL = GetAlertPolicyURL(ptype)
        alertPolicyURL = alertPolicyURL + "/" + id
        response = c.delete(alertPolicyURL)
        return


#== CLI Commands ==

@click.command()
@click.option('-t', '--policytype', type=click.Choice(['webhook', 'email', 'pagerduty']), help='Policy type') 
def list(policytype):
    '''List all alert policies'''
    GetAlertPolicyList(policytype)


@click.command()
@click.argument('policy_id')
@click.argument('policy_type')
def details(policy_id, policy_type):
    '''Details for alert policy'''
    if policy_type == "webhook" or policy_type == "email" or policy_type == "pagerduty":
        GetAlertPolicyDetails(policy_id, policy_type)
        return
    
    print "Policy Type should be: webhook, email or pagerduty"
    return


@click.command()
@click.argument('policy_id')
@click.argument('policy_type')
def delete(policy_id, policy_type):
    ''' Delete Alert Policy'''
    if policy_type == "webhook" or policy_type == "email" or policy_type == "pagerduty":
        DeleteAlertPolicy(policy_id, policy_type)
        return
    
    print "Policy Type should be: webhook, email or pagerduty"
    return


#== CLI Command Group ==

@click.group()
def policy():
    ''' Commands for alert policy '''
    pass

policy.add_command(list)
policy.add_command(details)
policy.add_command(delete)
	
