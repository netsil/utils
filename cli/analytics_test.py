import json
from analytics import *
#KEY WORDS for querystatement - input passed as "qs"
NAME = "name"
DATASOURCE = "datasource"
AGGREGATE = "aggregate"
GROUPBY = "group by"
FILTERS = "filters"

# Unit Test
qStmt = { NAME:"A", DATASOURCE:"http.request_response.latency", AGGREGATE:"avg", FILTERS: [{"field":"http.uri", "type":"isin", "value":"SQ1.A"},{"field":"http.uri", "type":"match", "value":"//httpblahblah"}, {"field":"http.uri", "type":"match", "value":"//httpblahblah"}, {"field":"http.status_code","type":"regex","value":"4dd|5dd"} ]  }
apiQ = CreateQuery(qStmt)
print json.dumps(apiQ)

evalStmt = { NAME:"B", "expr":"$A+$C+$D/$E*abs($F)"}
#print json.dumps(CreateEvalExpr(evalStmt))

rollingStmt= { NAME:"C", "reference":"D","aggregate":"sum","window":"30m" }

#print json.dumps(CreateRollingExpr(rollingStmt))

topnStmt= { NAME:"C", "reference":"E","aggregate":"sum","value":"10", "ascdsc":"asc" }

#print json.dumps(CreateTopnExpr(topnStmt))

#print (CreateSubQueryFilterScope(["SQ1.V"]))
