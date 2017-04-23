import json
import requests
from qparser import QueryStringParser
from analytics import CreateQuery
import time 
from aocurls import *
import requests
from requests import session
from botutils import *
from makeChart import *

def PostQuery(query):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        #print json.dumps(query)
        #fp=file('queryoutput.json','w')
        #fp.write(json.dumps(query, indent=4, sort_keys=True))
        resp = c.post(GetQueryPostURL(),json=query)
        #print resp.text
        #print json.dumps(resp.json(), indent=4, sort_keys=True)
        #fq=file('responseoutput.json','w')
        #fq.write(json.dumps(resp.json(), indent=4, sort_keys=True))
        return make_chart(resp.json())
        


def CreateQueryFromFile(qfile, interval, granularity):
    print "I will create query from file: " + qfile
    return {}

def CreateQueryFromString(qstr, interval, granularity):
    qs = QueryStringParser(qstr)
    #print qs
    tmpQueries = CreateQuery(qs)
    queries = {}
    queries["queries"] = tmpQueries["queries"]
    queries["type_propname"] = "_type"

    if qs.has_key("granularity"):
        if qs["granularity"]>0:
            granularity = qs["granularity"]
    queries["granularity_hint"] = granularity

    l = []
    if qs.has_key("timeinterval"):
        if qs["timeinterval"]>0:
            customIntervalInMS = PrepareTimeInterval(qs["timeinterval"]/1000, 0, 's')
            l.append(customIntervalInMS)
        else:
            l.append(interval)
    queries["queries"][0]["value"]["statements"][0]["value"]["query"]["options"]["INTERVALS"]=l
    return PostQuery(queries)

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

'''
start: default=300, help="start time for query specified as (now - s). default is 600" 
end: default=0, help="end time for query specified as (now - e). default is 0"
unit: type=click.Choice(['s','m','h','d']), default='s', help="time unit for the interval and granularity. can be s|m|h|d. default is s"
granularity: default=60, help="granularity of data. default is 60"
'''
def RunQuery(file='', start=300, end=0, unit='s', granularity=60, query=''):
    ''' Run Query '''
    intervalInMS = PrepareTimeInterval(start, end, unit)
    granularityInMS = PrepareGranularity(granularity, unit)
    if file:
        return CreateQueryFromFile(query, intervalInMS, granularityInMS)
    else:
        return CreateQueryFromString(query, intervalInMS, granularityInMS)

