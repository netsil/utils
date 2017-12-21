import click
import json
import requests
from requests import session
from aocurls import *
from cliutils import PrettyPrint
import random
import math
from qparser import QueryStringParser
from analytics import CreateQuery
from analytics import CreateQueriesFromStringList


#hack to generate the widget id since this is generated client side in the UI
def generateId():
    id = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    for i in range(0, 5):
        idx = int(math.floor(random.random() * len(possible)))
        id += possible[idx]

    return id

def DeleteDashboard(dbid):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        dbURL = GetDashboardURL()
        dbURL = dbURL + "/" + dbid
        response = c.delete(dbURL)
        print response        
        return 

def GetDashboard(keys, dbid):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetDashboardURL()+"/"+dbid)
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


def GetDashboardList(verbose):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetDashboardURL())
        parsed = json.loads(response.text)
        if verbose > 1:
            print json.dumps(parsed, indent=4, sort_keys=True)
            return
        alertCount = 0
        PrettyPrint(parsed, ["id", "dashboardName"])
        return
    

def CreateDashboard(name):
    db = { "spec": {"widgets":{}, "name":name} }

    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        dashboardURL = GetDashboardURL()
        response = c.post(dashboardURL, json=db)
        parsed = json.loads(response.text)
        print json.dumps(parsed, indent=4, sort_keys=True)
        return parsed 

def AddChart(plot, dashboard_id, name, query):
    tmpQueries = CreateQueriesFromStringList(query, True)
    chart = {}
    chart["reportSpecs"] = tmpQueries["queries"]
    vizSpecs = {}
    plotType = plot + "-chart"
    vizSpecs["selectedReferences"]=tmpQueries["queryNames"]
    vizSpecs["labels"]={}
    vizSpecs["chartTypes"]={"main query":plotType}
    vizSpecs["chartTitle"]= name
    vizSpecs["position"]= { "row":0, "col":0, "size_x":1, "size_y":1 }
    chart["vizSpecs"]=vizSpecs
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        dashboardURL = GetDashboardURL()+"/"+dashboard_id
        response = c.get(dashboardURL)
        db = json.loads(response.text)
        chartId = generateId()
        rowPosition = len(db["spec"]["widgets"].keys())
        chart["vizSpecs"]["position"]["row"]=rowPosition
        db["spec"]["widgets"][chartId]=chart
        response = c.post(dashboardURL, json=db)
        parsed = json.loads(response.text)
        print(parsed)
        #print json.dumps(parsed, indent=4, sort_keys=True)
        return parsed


@click.command()
@click.argument('dashboardid')
def delete(dashboardid):
    ''' Delete Dashboard '''
    if click.confirm("Do you want to delete the dashboard?"):
        DeleteDashboard(dashboardid)

@click.command()
@click.option('-k','--key', multiple=True, help='List of attributes to print. Print all if an attribute is not found')
@click.argument('dashboardid')
def get(key, dashboardid):
    ''' Get Dashboard '''

    GetDashboard(key, dashboardid)


@click.command()
@click.option('-v', '--verbose', default=1, help='Verbose level 1 (id, name); > 1 (all)')
def list(verbose):
    '''List all alerts '''
    GetDashboardList(verbose)


@click.command()
@click.argument('name')
def create(name):
    ''' Create Dashboard '''

    CreateDashboard(name)

@click.command()
@click.option('-p', '--plot', type=click.Choice(['line','area','stack-bar','bar', 'table', 'pie', 'gauge']), default='line', help='Chart plot type')
@click.argument('dashboard_id')
@click.argument('name')
@click.argument('query', nargs=-1)
def addchart(plot, dashboard_id, name, query):
    ''' Add Chart to Dashboard '''
    AddChart(plot, dashboard_id, name, query)
    #CreateQueriesFromStringList(query, True)

@click.group()
def dashboard():
    ''' Netsil AOC Dashboard Commands '''
    pass

dashboard.add_command(create)
dashboard.add_command(list)
dashboard.add_command(get)
dashboard.add_command(delete)
dashboard.add_command(addchart)

