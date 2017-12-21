import click
import json
import requests
from qparser import QueryStringParser
from analytics import CreateQuery
import time 
from aocurls import *
import requests
from requests import session

def PostQuery(query):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        #print json.dumps(query)
        resp = c.post(GetQueryPostURL(),json=query)
        print json.dumps(resp.json(), indent=4, sort_keys=True)
        return 

def CreateQueryFromFile(qfile, interval, granularity):
    print "NOT YET IMPLEMENTED TO BUILD QUERY FROM FILE " + qfile
    return {}

def CreateQueryFromString(qstr, interval, granularity):
    qstr = "A="+qstr
    qs = QueryStringParser(qstr)
    #print qs
    tmpQueries = CreateQuery(qs)
    queries = {}
    queries["queries"] = tmpQueries["queries"]
    queries["type_propname"] = "_type"
    queries["granularity_hint"]= granularity
    l = []
    l.append(interval)
    queries["queries"][0]["value"]["statements"][0]["value"]["query"]["options"]["INTERVALS"]=l
    #print(queries)
    PostQuery(queries)
    return

def ConvertToMS(unit):
    if unit == "s":
        return 1000
    if unit == "m":
        return 60 * 1000
    if unit == "h":
        return 60 * 60 * 1000
    if unit == "d":
        return 24 * 60 * 60 * 1000

def PrepareTimeInterval(start, end, unit):
    now = time.time()
    interval = []
    msConv = ConvertToMS(unit)
    interval.append( now * 1000 - start * msConv )
    interval.append( now * 1000 - end * msConv )
    return interval

def PrepareGranularity(granularity, unit):
    return granularity * ConvertToMS(unit)

#== CLI Commands ==
@click.command()
@click.option('-f','--filename', is_flag=True)
@click.option('-s','--start', default=300, help="start time for query specified as (now - s). default is 300" )
@click.option('-e','--end', default=0, help="end time for query specified as (now - e). default is 0")
@click.option('-u','--unit', type=click.Choice(['s','m','h','d']), default='s', help="time unit for the interval and granularity. can be s|m|h|d. default is s")
@click.option('-g','--granularity', default=60, help="granularity of data. default is 60")
@click.argument('query')
def run(filename, start, end, unit, granularity, query):
    ''' Run Query '''

    intervalInMS = PrepareTimeInterval(start, end, unit)
    granularityInMS = PrepareGranularity(granularity, unit)
    if filename:
        CreateQueryFromFile(query, intervalInMS, granularityInMS)
    else:
        CreateQueryFromString(query, intervalInMS, granularityInMS)

#== CLI Command Group ==
@click.group()
def query():
    ''' Netsil AOC Query Commands '''
    pass

query.add_command(run)

