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
import sys


#hack to generate the widget id since this is generated client side in the UI
def generateId():
    id = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    for i in range(0, 5):
        idx = int(math.floor(random.random() * len(possible)))
        id += possible[idx]

    return id

def DeleteDashboard(dbidlist):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        for dbid in dbidlist:
            print "Deleting Dashboard " + dbid
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
        return parsed


def GetDashboardList(verbose=0, name=None):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        response = c.get(GetDashboardURL())
        parsed = json.loads(response.text)
  
        idlist = ""
        if name != None:
            subset = []
            for m in parsed:
                if name in m["dashboardName"]:
                    idlist = idlist + m["id"] + " "
                    subset.append(m)
            parsed = subset

        if verbose==0:
            return parsed
        
        if verbose > 1:
            print json.dumps(parsed, indent=4, sort_keys=True)
        else:
            PrettyPrint(parsed, ["id", "dashboardName"])

        if name != None:
            print "Dashboard Ids with names containing: " + name
            print idlist
        
        return parsed
    

def CreateDashboard(name):
    db = { "spec": {"widgets":{}, "name":name} }

    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        dashboardURL = GetDashboardURL()
        response = c.post(dashboardURL, json=db)
        parsed = json.loads(response.text)
        #print json.dumps(parsed, indent=4, sort_keys=True)
        print "Created Dashboard:"
        print "name: " + parsed["dashboardName"] + ", id: " + parsed["id"] 
        return parsed 

def AddChart(plot, dashboard_id, name, query):
    tmpQueries = CreateQueriesFromStringList(query, True)
    chart = {}
    chart["reportSpecs"] = tmpQueries["queries"]
    vizSpecs = {}
    plotType = plot + "-chart"
    vizSpecs["selectedReferences"]=tmpQueries["queryNames"]
    vizSpecs["labels"]={"main query":tmpQueries["labels"]}
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
        #print json.dumps(parsed, indent=4, sort_keys=True)
        return parsed

def WriteDB(dbs, fname):
    try:
        with open(fname,"w") as fh:
                fh.write(json.dumps(dbs))
                fh.write("\n")
                fh.close()
    except IOError as e:
        print "Unable to open file: " + fname #Does not exist OR no read permissions
        sys.exit(1)

def ReadDB(fname):
    try:
        with open(fname,"r") as fh:
                dbs = json.loads(fh.readline())
                fh.close()
                return dbs
    except IOError as e:
        print "Unable to open file: " + fname #Does not exist OR no read permissions
        sys.exit(1)


def ExportDashboard(fname, ids):
    dbs = GetDashboardList()
    if len(ids) == 0:
        print "Exporting All Dashboards to " + fname
        WriteDB(dbs, fname)
        return
    
    toExport = []
    for db in dbs:
        dbid = db["id"]
        if dbid in ids:
            print "Exporting Dashboard Id = " + dbid + ", Name = " + db["dashboardName"]
            toExport.append(db)
    WriteDB(toExport, fname)
    return

def ImportDashboard(fname):
    dbs = ReadDB(fname)
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        dashboardURL = GetDashboardURL()
        for db in dbs:
            db.pop("id",None)
            print "Importing " + db["dashboardName"]
            response = c.post(dashboardURL, json=db)


@click.command()
@click.argument('dashboardid', nargs=-1)
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
@click.option('-n', '--name', help='Provide substring to look for in the name of dashboard')
def list(verbose, name):
    '''List All Dashboards '''
    GetDashboardList(verbose, name)


@click.command()
@click.argument('name')
def create(name):
    ''' Create Dashboard '''

    CreateDashboard(name)

@click.command()
@click.option('-p', '--plot', type=click.Choice(['line','area','stack-bar','bar', 'table', 'pie', 'gauge']), default='line', help='Chart plot type', show_default=True)
@click.argument('dashboard_id')
@click.argument('name')
@click.argument('query', nargs=-1)
def addchart(plot, dashboard_id, name, query):
    ''' Add Chart to Dashboard '''
    if query == None or len(query) == 0:
        print "Provide at least 1 query to create the chart"
        print "Input received dashboard id: " + dashboard_id + " name: " + name
        return
    AddChart(plot, dashboard_id, name, query)

@click.command()
@click.argument('filename')
@click.argument('ids', nargs=-1)
def exp(filename, ids):
    ''' Save Dashboards To File '''
    ExportDashboard(filename, ids)

@click.command()
@click.argument('filename')
def imp(filename):
    ''' Create Dashboards From File '''
    ImportDashboard(filename)


@click.group()
def dashboard():
    ''' Netsil AOC Dashboard Commands '''
    pass

dashboard.add_command(create)
dashboard.add_command(list)
dashboard.add_command(get)
dashboard.add_command(delete)
dashboard.add_command(addchart)
dashboard.add_command(exp)
dashboard.add_command(imp)


