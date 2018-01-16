from __future__ import unicode_literals, print_function
from pypeg2 import *
import re


#Global Keywords
MAIN_QUERY = "main_query"
SUB_QUERY = "sub_query"

class QSName(str):
    grammar = re.compile(r"[A-Z]+")

class Aggregate(str):
    grammar = re.compile(r"[a-zA-Z0-9]+")

class Datasource(str):
    grammar = re.compile(r"[a-zA-Z0-9\.\_\-]+")

class FilterOp(str):
    grammar = re.compile(r"[=|~|+]")

class FilterAttr(str):
    grammar = re.compile(r"[a-zA-Z0-9\.\_\-]+")

class FilterValue(str):
    grammar = re.compile(r"[a-zA-Z0-9\.\_\-\?\)\(\[\]\+\:\@\#\$\%\^\&\*\!\=\/\/]+")

class Filter(List):
    grammar = attr("field", FilterAttr), attr("type", FilterOp), attr("value", FilterValue)

def FiltertoDict(f):
    fDict = {}
    fDict["field"] = f.field
    fDict["type"] = f.type
    fDict["value"] = f.value
    return fDict


class Filters(List):
    grammar = "{", optional(csl(Filter)), "}"

class TimeRollup(str):
    grammar = "[", Aggregate, "]"

class TopKeyword(Keyword):
    grammar = Enum(Keyword("top"))

class TopValue(str):
    grammar = re.compile(r"[1-9][0-9]*")

class TopFunction(str):
    grammar = "," , Aggregate

class Top(List):
    grammar = attr("keyword", TopKeyword), "(", attr("value", TopValue) , attr("aggregate", optional(TopFunction)) , ")"

def ToptoDict(top):
    topDict = {}
    topDict["value"] = top.value
    if top.aggregate!=None:
        topDict["aggregate"] = top.aggregate
    return topDict

class GroupByKeyword(Keyword):
    grammar = Enum( Keyword("by") )

class GroupBy(List):
    grammar = attr("keyword",GroupByKeyword), "(", optional(csl(FilterAttr)), ")", attr("top", optional(Top))


class TimeshiftKeyword(Keyword):
    grammar = Enum( Keyword("timeshift"), Keyword("offset") )

class TimeshiftValue(str):
    grammar = re.compile(r"[0-9]+[s|m|h|d|w]")

def TSValueInMS(tsStr):
    l = len(tsStr)
    unit = tsStr[l-1:]
    v = tsStr[:l-1]
    value = int(v)
    if unit == "s":
        return value * 1000
    if unit == "m":
        return value * 60 * 1000
    if unit == "h":
        return value * 60 * 60 * 1000
    if unit == "d":
        return value * 24 * 60 * 60 * 1000
    if unit == "w":
        return value * 7 * 24 * 60 * 60 * 1000
    return 0
    
class Timeshift(List):
    grammar = attr("keyword", TimeshiftKeyword), "(", attr("value", TimeshiftValue), ")"

class LabelKeyword(Keyword):
    grammar = Enum ( Keyword("label") )

class LabelValue(str):
    grammar = re.compile(r"[a-zA-Z0-9\.\_\-]+")

class Label(List):
    grammar = attr("keyword", LabelKeyword), "(", attr("value", LabelValue), ")"

# Query Syntax  "A = avg(http.request_response.latency { http.uri ~ "/catalogue" }) by (client.pod_name) top(20) offset 1h"
class QS(List):
    grammar = attr("name", QSName), "=", attr("aggregate", Aggregate), "(", attr("datasource", Datasource), attr("filters", optional(Filters)), attr("timerollup",optional(TimeRollup)), ")", \
			attr("groupby", optional(GroupBy)), attr("timeshift", optional(Timeshift)), attr("label", optional(Label))
  
#convert the qs object to dictionary
def QStoDict(qs):
    qsDict = {}
    qsDict["name"] = qs.name
    qsDict["aggregate"] = qs.aggregate
    qsDict["datasource"] = qs.datasource
    
    qsDict["filters"] = []
    if qs.filters != None:   
        for f in qs.filters:
            qsDict["filters"].append(FiltertoDict(f))
            
    qsDict["timerollup"]= ""

    if qs.timerollup != None:
        qsDict["timerollup"] = qs.timerollup

    qsDict["groupby"] = []
    if qs.groupby != None:
        for attr in qs.groupby:
            qsDict["groupby"].append(attr)

        if qs.groupby.top != None:
            topDict = ToptoDict(qs.groupby.top)
            if "aggregate" not in topDict.keys():
                topDict["aggregate"]=qs.aggregate
            qsDict["top"]=topDict

            
    qsDict["timeshift"]=0
    if qs.timeshift != None:
        qsDict["timeshift"] = TSValueInMS(qs.timeshift.value)

    qsDict["label"]= qs.name
    if qs.label != None:
        qsDict["label"] = qs.label.value
    
    return qsDict

  

class Reference(str):
    grammar = re.compile(r"\$[A-Z]+")

class EvalExprKeyword(Keyword):
    grammar = Enum(Keyword("eval"))

class EvalExpr(str):
    grammar = re.compile(r"[a-zA-Z0-9\$\+\-\*\.\_\(\)\/]+")

# A = eval[expression] 
class ES(List):
    grammar = attr("name", QSName), "=", attr("keyword", EvalExprKeyword), "[", attr("expr", EvalExpr), "]" , attr("label", optional(Label))



def EStoDict(es):
    esDict = {}
    esDict["name"] = es.name
    esDict["expr"] = es.expr
    esDict["label"]= es.name
    if es.label != None:
        esDict["label"] = es.label.value

    return esDict

class RollingExprKeyword(Keyword):
    grammar = Enum(Keyword("rolling"))

class RollingExprWindow(str):
    grammar = re.compile(r"[1-9][0-9]*[s|m|h|d]")

class RollingStmt(List):
    grammar = attr("name", QSName), "=", attr("keyword", RollingExprKeyword), "[", attr("aggregate", Aggregate), ",", \
              attr("reference", Reference), ",", attr("window", RollingExprWindow), "]"

class TopnExprKeyword(Keyword):
    grammar = Enum(Keyword("topn"))

class TopnAscDsc(Keyword):
    grammar = Enum(Keyword("asc"), Keyword("dsc"))

class TopnStmt(List):
    grammar = attr("name", QSName), "=", attr("keyword", TopnExprKeyword), "[", attr("aggregate", Aggregate), ",", \
              attr("reference", Reference), ",", attr("value", TopValue), "," , attr("ascdsc",TopnAscDsc), "]"


class MQKeyword(Keyword):
    grammar = Enum(Keyword("main_query"))

class MQTime(str):
    grammar = re.compile(r"[0-9\:\-\.TZsmhd]+")

class MQTimeInterval(List):
    grammar = "[", attr("start", MQTime), "," , attr("end",optional(MQTime))  , "]"

class MQGranularity(str):
    grammar = "[", re.compile(r"[1-9][0-9]*[s|m|h|d]"), "]"

class MQDataReturnStmt(List):
    grammar = "[", QSName , maybe_some(",", QSName), "]"

class MQSection(List):
    grammar = attr("keyword", MQKeyword), ":", MQTimeInterval, maybe_some(",",MQTimeInterval), attr("granularity",MQGranularity), attr("return_list",MQDataReturnStmt)


class SQName(str):
    grammar = re.compile(r"SQ[1-9]+")

class SQKeyword(Keyword):
    grammar = Enum(Keyword("sub_query"))

class SQSection(List):
    grammar = attr("keyword", SQKeyword), ":" , attr("name", SQName) ,",", attr("return_stmt", QSName)
 

def QueryStringParser(qstr):
    qs = parse(qstr, QS)
    return QStoDict(qs)

def EvalStringParser(qstr):
    qs = parse(qstr, ES)
    return EStoDict(qs)
