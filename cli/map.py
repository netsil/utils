import click
import time
import requests
from requests import session
import json
from aocurls import *
from cliutils import PrettyPrint
from graph import *
import math
import random

def GetMapFileName(mapname):
    return mapname+".map"

def generateFilterId():
    n = 15
    id = ''
    possible = '0123456789'
    for i in range(0, n):
        idx = int(math.floor(random.random() * len(possible)))
        id += possible[idx]
    return id


def ConvertToMS(unit):
    if unit == "s":
        return 1000
    if unit == "m":
        return 60 * 1000
    if unit == "h":
        return 60 * 60 * 1000
    if unit == "d":
        return 24 * 60 * 60 * 1000

def PrepareTimeInterval(maptime, timeinterval, unit):
    now = time.time()
    interval = []
    msConv = ConvertToMS(unit)
    t1 = now * 1000 - maptime * msConv 
    t2 = t1 - timeinterval * ConvertToMS("m")
    interval.append( t2 )
    interval.append( t1 )
    return interval

def TransformFilter(f):
    tmpFilter = {}
    tmpFilter["key"]= f["key"]
    tmpFilter["type"] = f["type"]
    if "filterValue" in f.keys():
        tmpFilter["value"]={}
        tmpFilter["value"]["text"]= f["filterValue"] 
    return tmpFilter

def CreateFilter(type, key, value, name):
    f = {}
    f["id"] = generateFilterId()
    f["name"]= name
    f["filterValue"]= value
    f["selectedValue"]= value
    f["type"]=type
    f["key"]=key
    return f

def ParseAndCreateFilter(f):
    mf = f.split("=")
    if len(mf) >= 2:
        return CreateFilter("match", mf[0].strip(), mf[1].strip(), f)

    rf = f.split("~")
    if len(rf) >= 2:
        return CreateFilter("regex", rf[0].strip(), rf[1].strip(), f)
   
    return {}

def ParseFilterList(filters):
    flist = []
    for f in filters:
        flist.append(ParseAndCreateFilter(f))
    return flist

def ParseGroupByList(groupby):
    byList = []
    for x in groupby:
        byList.append(x.strip())
    return byList


def CreateMapFilter(filters):
    if len(filters) <= 0:
        return {}
    groupByField = {}
    returnObject = {}
    for filter in filters:

        tmpFilter = TransformFilter(filter)
        if not tmpFilter:
            continue

        if "key" not in tmpFilter.keys():
            continue

        field = tmpFilter["key"]
        if field not in groupByField.keys():
           groupByField[field]= []
        groupByField[field].append(tmpFilter)

    orList = []
    for key in groupByField.keys():
        orFilter = {}
        if len(groupByField[key]) > 1:
            orFilter["type"] = "or"
            orFilter["fields"] = []
            for f in groupByField[key]:
                orFilter["fields"].append(f)
        else:
            orFilter = groupByField[key][0]
        orList.append(orFilter)
    
    if len(orList) == 1:
        return orList[0]

    if len(orList) > 1:
        returnObject = {}
        returnObject["type"] = "and"
        returnObject["fields"] = []
        for f in orList:
            returnObject["fields"].append(f)
        return returnObject

    return {}




#==== Map Graph Related Wrapper Functions ====
def FindNodes(g, nodes):
    nodeList=[]
    for n in g.nodes():
        for sub in nodes:
            if sub in n:
                nodeList.append(n)
                break
    return nodeList

def DescribeMap(name):
    g = ReadGraph(GetMapFileName(name))
    PrintGraph(g)
    return g

def GetEdges(exact, direction, name, nodes):
    g = ReadGraph(GetMapFileName(name))
    nodeList = nodes
    if not exact:
        nodeList = FindNodes(g, nodes)
    edges = []
    if direction == "in" or direction == "all":
        edges = edges + GetInEdges(g, nodeList)

    if direction == "out" or direction == "all":
        edges = edges + GetOutEdges(g, nodeList)
    
    PrintEdges(edges)
    return edges


def GetPaths(name, source, target, submap):
    g = ReadGraph(GetMapFileName(name))
    src = FindNodes(g, [source])
    if len(src) == 0:
        print "Did Not Find Source Node: " + source
        return []
    tgt = FindNodes(g, [target])
    if len(tgt) == 0:
        print "Did Not Find Source Node: " + target
        return []
    
    paths = GetSimplePaths(g, src[0], tgt[0])
    PrintPaths(paths)
    
    if submap != None:
        nodes = MergeNodes(paths)
        CreateSubMap(nodes, name, submap)

    return paths


def GetTree(submap, depth, type, name, source):
   g = ReadGraph(GetMapFileName(name))
   src = FindNodes(g, [source])
   if len(src) == 0:
       print "Did Not Find Source Node: " + source
       return []
   tree = GetTreeEdges(g, src[0], type, depth)
   PrintEdges(tree)

   if submap != None:
       nodes = MergeNodes(tree)
       CreateSubMap(nodes, name, submap)

   return tree


def CreateLocalGraph(m, attributes):
    name = attributes["name"]
    g= MakeGraph(m)
    fname = GetMapFileName(name)
    WriteGraph(g, attributes, fname)
    PrintGraph(g)
    return g

#==== Map related get and post functions =====

# create a sub map with specified nodes and attributes from an existing map
def CreateSubMap(nodes, parentmap, name):
    attributes = ReadGraphAttr(GetMapFileName(parentmap))
    groupby = attributes["groupBys"]
    filterAttr = []
    for n in nodes:
        filterAttr.append(GetNodeAttr(n, groupby))

    newFilters = []
    for attr in filterAttr:
        for key in attr.keys():
            newFilters.append(str(key + "=" + attr[key]))
    sm = CreateMap(groupby, newFilters, name, "merge")
    print {"name":sm["name"], "id":sm["id"]}
    return sm



def CreateMap(groupby, filter, name, remaining="auto"):
    mapOptions = {}
    mapOptions["name"]=name
    mapOptions["filters"]=ParseFilterList(filter)
    mapOptions["groupBys"]=ParseGroupByList(groupby)
    mapOptions["remaining"]=remaining
    mapOptions["defaultView"]="topology"
    mapOptions["TopologyMapGroupingRules"]=[]
    mapOptions["showLinks"]=True
    mapOptions["showLinkMetrics"]=True
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        topoURL = GetTopologyMapURL()
        response = c.post(topoURL, json=mapOptions)
        #print response.json()
        parsed = json.loads(response.text)
        #print json.dumps(parsed, indent=4, sort_keys=True)        
        return parsed

def GetMapAttributes(id):
    with session() as c:    
        c.post(GetAuthURL(), data=GetCredentials())
        topoURL = GetTopologyMapURL()+"/"+id
        response = c.get(topoURL)
        parsed = json.loads(response.text)
        #print json.dumps(parsed, indent=4, sort_keys=True)
        return parsed

def GetMap(attributes, timeinterval):
    mapQuery = {}
    mapOptions = {}
    mapOptions["clustering"]=True
    mapOptions["FILTER"]=CreateMapFilter(attributes["filters"])
    mapOptions["groupby"]=attributes["groupBys"]
    mapOptions["remaining"]=attributes["remaining"]

    mapOptions["services"]=[]
    mapOptions["INTERVALS"]=[]
    mapOptions["INTERVALS"].append(timeinterval)
    mapOptions["misc"]={"_TIMESTAMP_MIN":timeinterval[0], "GRANULARITY":1000}
    mapOptions["LIMIT"]={"column":"count","value":5}
    mapQuery["options"]=mapOptions
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        mapURL = GetMapURL()
        response = c.post(mapURL, json=mapQuery)
        #print response.json()
        parsed = json.loads(response.text)
        #print json.dumps(parsed, indent=4, sort_keys=True)
        return parsed



def CreateMapAndSaveLocalGraph(groupby, filter, timeinterval, name):
    mapAttributes = CreateMap(groupby, filter, name)
    m = GetMap(mapAttributes, timeinterval)
    mapAttributes["interval"] = timeinterval
    g = CreateLocalGraph(m, mapAttributes)
    return g


def GetMapAndSaveLocalGraph(id, timeinterval):
    mapAttributes = GetMapAttributes(id)
    m = GetMap(mapAttributes, timeinterval)
    mapAttributes["interval"] = timeinterval
    g = CreateLocalGraph(m, mapAttributes)
    return g


def ListMap():
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        topoURL = GetTopologyMapURL()
        response = c.get(topoURL)
        parsed = json.loads(response.text)
        PrettyPrint(parsed, ["id", "name"])
        return parsed

def DeleteMap(mapid):
    with session() as c:
        c.post(GetAuthURL(), data=GetCredentials())
        topoURL = GetTopologyMapURL()+"/"+mapid
        response = c.delete(topoURL)
        print response
        return


#== CLI Commands ==
@click.command()
@click.option('-t','--maptime', default=0, help="Start time for getting the map specified as (now - t)", show_default=True )
@click.option('-i','--interval', type=click.Choice(['1', '5', '10', '30', '60']), default='10', help="Time interval in minutes. time - interval", show_default=True)
@click.option('-u','--unit', type=click.Choice(['m','h','d']), default='m', help="Time unit for the time. can be min, hr, day", show_default=True)
@click.option('-f','--filter', multiple=True, help="Provide filters as attribute=value or attribute~value, the ~ will do regex")
@click.option('-g','--groupby', multiple=True, help="Groupby criteria defining the nodes in the map e.g. pod_name, host_name, tags.kube_app, etc.")
@click.argument('name')
def create(maptime, interval, unit, filter, groupby, name):
    ''' Create Map & Save Locally In <Name.map> File '''
    if interval != None:
        interval = int(interval)
    timeinterval = PrepareTimeInterval(maptime, interval, unit)
    CreateMapAndSaveLocalGraph(groupby, filter, timeinterval, name)

@click.command()
@click.option('-t','--maptime', default=0, help="Start time for getting the map specified as (now - t)" , show_default=True)
@click.option('-i','--interval', type=click.Choice(['1', '5', '10', '30', '60']), default='10', help="Time interval in minutes. time - interval", show_default=True)
@click.option('-u','--unit', type=click.Choice(['m','h','d']), default='m', help="Time unit for the time. can be min, hr, day", show_default=True)
@click.argument('id')
def get(maptime, interval, unit, id):
    ''' Get Map & Update Local Copy '''
    if interval != None:
        interval = int(interval)
    timeinterval = PrepareTimeInterval(maptime, interval, unit)
    GetMapAndSaveLocalGraph(id, timeinterval)


@click.command()
@click.option('-e', '--exact', default=False, type=bool, help='Only use nodes with exact match otherwise treat input as substring match', show_default=True)
@click.option('-d', '--direction', type=click.Choice(['in','out', 'all']), default='all', help='Get in, out or all edges for given nodes', show_default=True) 
@click.argument('name')
@click.argument('nodes', nargs=-1)
def edges(exact, direction, name, nodes):
    ''' Get Edges For Nodes '''
    GetEdges(exact, direction, name, nodes)

@click.command()
@click.option('-s', '--submap', help='Name of submap based on the nodes')
@click.argument('name')
@click.argument('source')
@click.argument('target')
def paths(submap, name, source, target):
    ''' Get Paths From Source To Target Node '''
    GetPaths(name, source, target, submap)


@click.command()
@click.option('-s', '--submap', help='Name of submap based on the nodes')
@click.option('-d', '--depth', type=click.INT, help="Depth limit for tree")
@click.option('-t', '--type', type=click.Choice(['bfs', 'dfs']), default='dfs', help='Tree traversal type breadth-first or depth-first', show_default=True)
@click.argument('name')
@click.argument('source')
def tree(submap, depth, type, name, source):
    ''' Get Traversal Tree From Source '''
    GetTree(submap, depth, type, name, source)


@click.command()
@click.argument('mapid')
def delete(mapid):
    ''' Delete the Map ''' 
    DeleteMap(mapid)

@click.command()
@click.argument('name')
def describe(name):
    ''' Get Map Details '''
    DescribeMap(name)

@click.command()
def list():
    ''' List All Maps '''
    ListMap()

@click.group()
def map():
    ''' Netsil AOC Map Commands '''
    pass

map.add_command(create)
map.add_command(delete)
map.add_command(edges)
map.add_command(paths)
map.add_command(tree)
map.add_command(describe)
map.add_command(list)
map.add_command(get)


