from dashboard import CreateDashboard, AddChart
from graph import GetEdges, GetNodes


K8s_DS = { 
        "memory":["kubernetes.memory.usage","kubernetes.memory.limits", "kubernetes.memory.requests"],
        "cpu": ["kubernetes.cpu.usage.total","kubernetes.cpu.limits", "kubernetes.cpu.requests"]
        }

Status_DS = {
        "http" : ["http.status.code","http.status.message"],
        "cassandra" : ["cassandra.error.code", "cassandra.error.string"],
        "mongodb" : ["mongodb.responsecode", "mongodb.responsecodename"],
        "mysql" : ["mysql.error.code", "mysql.error.string"],
        "postgresql" : ["postgresql.error.string"],
        "redis" : [ "redis.error.string", "redis.response.status" ],
        "memcached" : ["memcached.response"],
        "http2": ["http2.status", "http2.grpcstatus", "http2.grpcmessage"]
        }




Proto_DS = [ { "agg":"avg", "ds":"request_response.latency"}, {"agg":"throughput", "ds": "request_response.throughput"} ]


def CreateFilterForEdges(edges, attributes):
    fs = ""
    for e in edges:
        client = e[0]
        server = e[1]
        for attr in attributes:
            if attr in client.keys():
                fs = fs + " client." + attr + "=" + client[attr] + " ,"
            if attr in server.keys():
                fs = fs + " server." + attr + "=" + server[attr] + " ,"
    if len(fs) > 0:
        fs = fs[:-1]
        fs = "{ " + fs + " }"

    return fs
           

def CreateGroupbyForEdges(attributes, extra=None):
    groupby = ""
    for attr in attributes:
        groupby = groupby + " client." + attr + " ,"
        groupby = groupby + " server." + attr + " ,"
    if extra != None:
        for attr in extra:
            groupby = groupby + " " + attr + " ,"

    if len(groupby) > 0:
        groupby = groupby[:-1]
        groupby = " by ("+ groupby + ")"
    return groupby
            

def EdgeDashboard(graph, attributes, dbid):
    fields = attributes["groupBys"]
    groupby = CreateGroupbyForEdges(fields)
    edges = GetEdges(graph, True)
    print edges 
    for e in edges:
        if len(e) == 3:
            attr = e[2]
            if "protocols" in attr.keys():
                filters = CreateFilterForEdges([e], fields)
                for proto in attr["protocols"]:
                    if proto == "protocol":
                        continue
                    if proto == "uri":
                        proto = "http"
                    queries = []
                    for metric in Proto_DS:
                        qs = metric["agg"] + "( " + proto + "." + metric["ds"] + " " + filters + " ) " + groupby
                        queries.append(qs)
                    chartname = proto 
                    print "Added chart : " + chartname
                    AddChart("table", dbid, chartname, queries)
                    
                    if proto in Status_DS.keys():
                        statusquery = "throughput( " + proto + ".request_response.throughput " + filters + " ) " +  CreateGroupbyForEdges(fields, Status_DS[proto])
                        chartname = proto + " status/errors " 
                        AddChart("table", dbid, chartname, [statusquery])




def GraphDashboard(graph, attributes, name):
    db = CreateDashboard(name)
    dbid = db["id"]
    print "Created Dashboard :"
    print "name: " + name + ", id:" + dbid
    EdgeDashboard(graph, attributes, dbid)






