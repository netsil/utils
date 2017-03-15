import re
import json
from cliutils import JSONLoadsString
import datetime
import pytz

SAFE_COUNT = 20

#KEY WORDS for querystatement - input passed as "qs"
NAME = "name"
DATASOURCE = "datasource"
AGGREGATE = "aggregate"
GROUPBY = "group by"
FILTERS = "filters"

#Granularity controls amount and also impacts asof_tolerance during alignment of time series; defaulted to 1min
__GRANULARITY_ = 60000
__EPOCH_TIME_ = datetime.datetime(1970,1,1,tzinfo=pytz.utc) 

def SetGranularity(granularity):
    __GRANULARITY_=granularity

def GetGranularity():
    return __GRANULARITY_

def CreateDataReference(queryNames):
    refObject = {}
    for queryName in queryNames:
        dataRef = {
            "data": {
                "dataframe": {
                    "name": queryName,
                    "_type": "reference"
                    },
                "ungrouped_cols": "INTERVAL",
                "aggregation": "count",
                "sort_by": "A",
                "n": SAFE_COUNT,
                "_type": "topn"
                },
            "metadata": {
                "value": {
                  "name": queryName,
                  "_type": "reference"
                },
                "_type": "inspect"
              }
            }
        refObject[queryName]=dataRef
    return refObject

# input is of the form ["SQ1.B", "SQ1.AA"] 
def CreateSubQueryFilterScope(sqList):
    scope={}
    for sq in sqList:
        sqDetails = sq.split(".")
        
        sqName = sqDetails[0]
        sqStmt = sqDetails[1]

        objs = []
        scope[sqName]= {
                    "objs":
                    [
                        {
                            "name":"data",
                            "scope":{
                                "name":sqStmt,
                                "scope":{
                                    "name":sqName,
                                    "_type":"reference"
                                    },
                                "_type":"reference"
                                },
                            "_type":"reference"
                        }
                    ],
                    "_type":"concat"
                }

    return scope 


def CreateGroupBy(attributes):
    groupByObject = {}
    groupByObject["XAXIS"]= "INTERVAL"
    if len(attributes) <= 0:
        groupByObject["SERIES_O"] = "none"
        return groupByObject

    for i, attribute in enumerate(attributes):
        series = "SERIES_" + str(i)
        groupByObject[series]=attribute

    return groupByObject

def CreateSQFilter(filter):
    sq=filter["value"]
    sqDetails = sq.split(".")
    sqName = sqDetails[0]
    sqStmt = sqDetails[1]
    tmpFilter = {
            "type":"isin",
            "column":filter["field"],
            "value":{
                "list":{
                    "to":"list",
                    "drop":[sqStmt, "INTERVAL"],
                    "data":{
                        "name":sqName,
                        "_type":"reference"
                        },
                    "_type":"cast"
                    }
                }
            }
    return tmpFilter

def CreateRegexFilter(filter):
    tmpFilter = {}
    tmpFilter["column"]= filter["field"]
    tmpFilter["value"]={}
    tmpFilter["value"]["text"]= filter["value"] 
    tmpFilter["type"] = "regex"
    return tmpFilter

def CreateMatchFilter(filter):
    tmpFilter = {}
    tmpFilter["column"]= filter["field"]
    tmpFilter["value"]={}
    tmpFilter["value"]["text"]= filter["value"] 
    tmpFilter["type"] = "match"
    return tmpFilter


# type: column: value: { text: }
def CreateFilter(filters):
    if len(filters) <= 0:
        return {}
    groupByField = {}
    returnObject = {}
    for filter in filters:
        tmpFilter = {}
        if filter["type"]=="match" or filter["type"]=="=":
            tmpFilter = CreateMatchFilter(filter)
        elif filter["type"]=="regex" or filter["type"]=="~":
            tmpFilter = CreateRegexFilter(filter)
        else:
            tmpFilter = CreateSQFilter(filter)

        field = filter["field"]
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


def CreateQueryOptions(qs):
   # Do sanity checks that qs has NAME and AGGREGATE keywords

    function = {
            "column":"",
            "aggregate": qs[AGGREGATE]
            }
    metrics = {}
    metrics[qs[NAME]] = function
    
    optionsObject = {}
    optionsObject["Metrics"]= metrics

    filters = {}
    if FILTERS in qs.keys():
        filters = qs[FILTERS]

    optionsObject["FILTER"]=CreateFilter(filters)

    groupByAttributes = []
    if "groupby" in qs.keys():
        groupByAttributes = qs["groupby"]

    optionsObject["GroupBy"]=CreateGroupBy(groupByAttributes)
    
    topObject = {"column":"no top n","value":0}
    if "top" in qs.keys():
        topObject["column"] = qs["top"]["aggregate"]
        topObject["value"] = qs["top"]["value"]
    
    optionsObject["LIMIT"]=topObject

        
    if "timeshift" in qs.keys():
        optionsObject["timeshift"]= qs["timeshift"]

    return optionsObject 


def CreateQueryStatement(qs):
   # should try /catch and bail out; fix this later

    if NAME not in qs.keys():
        return None
    if DATASOURCE not in qs.keys():
        return None
    if AGGREGATE not in qs.keys():
        return None


    queryStatement = {
            "name":qs[NAME],
            "value":{
                "query":{
                    "options":CreateQueryOptions(qs),
                    "report-name":qs[DATASOURCE]                    
                    },
                "_type":"netsil_query"
                },
            "_type":"assignment"
            }
    return queryStatement


def CreateQuery(qs):
    # Note that the return object is a python dictionary not a JSON object. 
    queries={}
    queries["queries"]= []
    
    query = {}
    query["name"]="main query"
    query["_type"]="assignment"

    statements=[]
    statements.append(CreateQueryStatement(qs))
    
    queryNames = []
    queryNames.append(qs["name"])
    statements.append(CreateDataReference(queryNames))

    valueObject = {}
    valueObject["statements"]=statements
    valueObject["_type"]="local_scope"
    # need to add scope object if there are subquery filters
    if FILTERS in qs.keys():
        sqFilters = []
        for f in qs[FILTERS]:
            if f["type"]=="isin" or f["type"]=="+":
                sqFilters.append(f["value"])
        if len(sqFilters) > 0:
            valueObject["scope"]=CreateSubQueryFilterScope(sqFilters)

    
    query["value"] = valueObject 
    
    queries["queries"].append(query)
    return queries

def CreateEvalDataFrame(labels):
    if len(labels) == 0:
        return None

    df = {}
    df["_type"]="reference"
    df["name"]=labels[0]
    if len(labels)==1:
        return df
    
    dfParent = {}
    dfParent["asof_on"]="INTERVAL"
    dfParent["asof_tolerance"]= GetGranularity() - 1
    dfParent["_type"]="join"
    dfParent["left"]=df
    dfParent["right"]=CreateEvalDataFrame(labels[1:])

    return dfParent


def CreateEvalExpr(evalExpr):
    
    if NAME not in evalExpr.keys():
        return None
    if "expr" not in evalExpr.keys():
        return None
    
    evalExprStatement = {
            "name": evalExpr[NAME],
            "value": {},
            "_type": "assignment"
          }
    valueObject = {} 
    valueObject["axis"]=1
    valueObject["_type"]="drop"
    refPattern = re.compile(r"\$[A-Z]+")
    references = re.findall(refPattern, evalExpr["expr"])
    labels = []
    for ref in references:
        labels.append(ref[1:])
    valueObject["labels"]=labels
    dfObject = {}
    dfObject["expr"] = evalExpr["name"]+ " = " + re.sub(r"\$","",evalExpr["expr"])
    dfObject["_type"] = "eval"
    dfObject["dataframe"]=CreateEvalDataFrame(labels)
    valueObject["dataframe"]=dfObject
    evalExprStatement["value"]=valueObject
    return evalExprStatement

def CreateRollingExpr(rollingExpr):
    if all (k in rollingExpr for k in ("name","reference", "aggregate", "window")):
        df = { "name": rollingExpr["reference"], "_type":"reference" }
        dfParent = {}
        dfParent["_type"]="rolling"
        dfParent["aggregation"]=rollingExpr["aggregate"]
        dfParent["columns"]=rollingExpr["reference"]
        dfParent["window"] = re.sub(r"m$","min",rollingExpr["window"])
        dfParent["dataframe"]=df

        valueObject = {}
        valueObject["columns"]={ rollingExpr["reference"]:rollingExpr["name"] }
        valueObject["dataframe"]=dfParent
        valueObject["_type"]="rename"
        returnObject = {}
        returnObject["name"] = rollingExpr["name"]
        returnObject["value"] = valueObject
        returnObject["_type"] = "assignment"
        return returnObject 

    return None

def CreateTopnExpr(topnExpr):
    if all (k in topnExpr for k in ("name","reference", "aggregate", "value")):
        df = { "name": topnExpr["reference"], "_type":"reference" }
        dfParent = {}
        dfParent["_type"]="topn"
        dfParent["n"]= topnExpr["value"]
        dfParent["sort_by"]=topnExpr["reference"]
        dfParent["ungrouped_cols"]= "INTERVAL"
        dfParent["aggregation"] = topnExpr["aggregate"]
    
        if "ascdsc" in topnExpr.keys() and topnExpr["ascdsc"]=="asc":
            dfParent["ascending"]="true"
        dfParent["dataframe"]=df
        
        valueObject = {}
        valueObject["columns"]={ topnExpr["reference"]:topnExpr["name"] }
        valueObject["dataframe"]=dfParent
        valueObject["_type"]="rename"
        returnObject = {}
        returnObject["name"] = topnExpr["name"]
        returnObject["value"] = valueObject
        returnObject["_type"] = "assignment"
        return returnObject 

    return None



