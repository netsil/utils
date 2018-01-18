import networkx as nx
from networkx.readwrite import json_graph
import json
from cliutils import *
import sys

# Takes the map coming from Netsil AOC and makes graph by extracting just the nodes and edges
def MakeGraph(m):
    g = nx.DiGraph()
    nodes = m["nodes"].keys()
    edges = []
    for e in m["links"]:
        protocols = e["metrics"].keys()
        attr = {"protocols":protocols}
        edges.append(list([e["source"],e["target"], attr]))
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    return g

def WriteGraph(g, mapOptions, fname):
    try:
        with open(fname,"w") as fh:
                data = json_graph.node_link_data(g)
                fh.write(json.dumps(data))
                fh.write("\n")
                fh.write(json.dumps(mapOptions))
                fh.write("\n")
                fh.close()
    except IOError as e:
        print "Unable to open file: " + fname #Does not exist OR no read permissions
        sys.exit(1)

def ReadGraph(fname):
    try:
        with open(fname,"r") as fh:
            data = json.loads(fh.readline())
            fh.close()
            return(json_graph.node_link_graph(data))
    except IOError as e:
        print "Unable to open file: " + fname #Does not exist OR no read permissions
        sys.exit(1)

def ReadGraphAttr(fname):
    try:
        with open(fname,"r") as fh:
            data = json.loads(fh.readline())
            attr = json.loads(fh.readline())
            fh.close()
            return(attr)
    except IOError as e:
        print "Unable to open file: " + fname #Does not exist OR no read permissions
        sys.exit(1)

def FindNodes(g, nodes):
    nodeList=[]
    for n in g.nodes():
        for sub in nodes:
            if sub in n:
                nodeList.append(n)
                break
    return nodeList

# Lower level graph extraction functions
# The node should be converted to dictionary using JSONLoadsString
# all upper level functions assume nodes to be dictionary

def MakeNode(n):
    return JSONLoadsString(n)

def MakeNodes(nodes):
    nodeList = []
    for n in nodes:
        nodeList.append(MakeNode(n))
    return nodeList

def MakeEdge(e):
    return [MakeNode(e[0]), MakeNode(e[1])]

def MakeEdges(edges):
    edgeList = []
    for e in edges:
        edgeList.append(MakeEdge(e))
    return edgeList


def GetOutEdges(g, nodes):
    edges = []
    for e in g.out_edges(nodes):
        edges.append(MakeEdge(e))
    return edges

def GetInEdges(g, nodes):
    edges = []
    for e in g.in_edges(nodes):
        edges.append(MakeEdge(e))
    return edges
    
def GetSimplePaths(g, src, tgt):
    pg = nx.all_simple_paths(g, src, tgt)
    paths = []
    for p in pg:
        path = []
        for n in p:
            path.append(MakeNode(n))
        paths.append(path)
    return paths

def GetTreeEdges(g, src, type, depth):
    edges = []
    if type == "dfs":
        for e in nx.dfs_edges(g, src, depth):
            edges.append(MakeEdge(e))
        return edges
    if type == "bfs":
        for e in nx.bfs_edges(g, src):
            print e
            edges.append(MakeEdge(e))
        return edges

    
def GetNodes(g):
    nodes = []
    for n in g.nodes():
        nodes.append(MakeNode(n))
    return nodes

def GetEdges(g, attr=False):
    edges = []
    for e in g.edges.data():
        tmp = MakeEdge(e)
        if attr:
            if len(e) == 3:
                tmp.append(e[2]) 
        edges.append(tmp)
    return edges

    
#==== Upper level functions. these assume nodes are a dictionary 

def PrintNodes(nodes):
    print "Nodes"
    print "====="
    for n in nodes:
        print n
    print "====="

def PrintEdges(edges):
    print "Edges"
    print "====="
    eObjs = []
    for e in edges:
        obj = {"client":e[0], "server":e[1]}
        eObjs.append(obj)
    PrettyPrint(eObjs)

def PrintPaths(paths):
    print "Paths"
    print "====="
    for p in paths:
        print p
    print "====="
    return

def PrintGraph(g):
    PrintNodes(GetNodes(g))
    PrintEdges(GetEdges(g))
    return

def GetNodeAttr(node, attributes):
    retObj = {}
    for attr in attributes:
        if attr in node.keys():
            retObj[attr]=node[attr]
    return retObj

def MergeNodes(nlistoflist):
    nodes = []
    for nl in nlistoflist:
        for n in nl:
            nodes.append(n)
    return nodes


