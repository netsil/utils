from __future__ import unicode_literals, print_function
from pypeg2 import * 
from qparser import *

sq = parse("sub_query:SQ19, BBN", SQSection)
print(sq.name)
print(sq.return_stmt)

mq = parse("main_query:[30m,][1m][A,B,C]",MQSection)
print(mq.granularity)
print(len(mq))
print(mq[0].start)

mq = parse("main_query:[2015-12-31T12:12:12Z, 2016-1-13T12:12:12Z][1m][A,B]",MQSection)
print(mq.granularity)
print(len(mq))
print(mq[0].start)
print(mq[0].end)

t = parse("top (5)", Top)
print("top")
print(t)
print(t.__dict__)
g = parse("by (httpuri)", GroupBy)
print("groupby")
print(g)
print(g.__dict__)

b = parse("A = sum(http.request_response.latency)", QS)
print ("simple query")
print (b)
print (b.__dict__)
print (hasattr(b,"filters"))


f = parse(" AAAA = sum ( http.request_response.latency {a=b, e=http://luba_duba.com/?, http.uri + SQ1} ) by (http.uri)  timeshift(30s) ", QS)

print(f.name)
print(f.aggregate)
print(f.datasource)

for filter in f.filters:
    print (filter.field)
    print (filter.type)
    print (filter.value)
print(len(f.filters))

for groupbyAttr in f.groupby:
    print (groupbyAttr)

print("Found timeshift")
print(f.timeshift.value)

filters = parse("{}", Filters)




filter = parse( " a=b ", Filter)
print (filter.field)
print (filter.type)
print (filter.value)



filters = parse( "{a=b, c=d, e=http://luba_duba@blahblah.com}", Filters)
print (len(filters))
for filter in filters:
	print (filter.field)
	print (filter.type)
	print (filter.value)
filters = parse("{}", Filters)
print (len(filters)) 

e1 = parse("A=eval[$B+$C+$D/$E*99.9*(2-$Y)+abs($B)]",EvalStmt)
print(e1.name)
print(e1.expr)

e2 = parse("ZXYZ=rolling[sum, $BBB, 30m]", RollingStmt)
print(e2.name)
print(e2.aggregate)
print(e2.reference)
print(e2.window)

e3 = parse("ABCDEYY=topn[sum, $BX, 5, asc]", TopnStmt)
print(e3.name)
print(e3.aggregate)
print(e3.reference)
print(e3.value)
print(e3.ascdsc)


f = QueryStringParser(" AAAA = sum ( http.request_response.latency {a=b, e=http://luba_duba.com/?, http.uri + SQ1} [avg] ) by (http.uri)  timeshift(30s) ")
print(f)
