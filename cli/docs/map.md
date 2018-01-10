## Working with Netsil Maps using CLI
Netsil Maps provide visibility into the dependency structure of the distributed applications. The maps are defined by two primary input:
1. groupby: List of attributes to use for defining the node of a map. For e.g. `pod_name`, `namespace`, `host_name`, `tags.kube_app`, etc.
2. filter: What values to include in the map. For e.g. namespace = sock-shop
Using the above two input, Netsil will leverage its service interaction data to create a map for any time interval including live map. 
From the CLI, you can note only create the maps by defining the above input but you can also save the map locally for analysis. Since the structure of an application does change every minute, this locally saved map provides a fast, efficient way of exploring the structure without having the run expensive calculations on the Netsil service. The following sections explain the steps of creating and using the maps in more details. 

# Creating Maps
``` bash
netsil map create --help
Usage: netsil map create [OPTIONS] NAME

  Create Map & Save Locally In <Name.map> File

Options:
  -t, --maptime INTEGER          Start time for getting the map specified as
                                 (now - t)  [default: 0]
  -i, --interval [1|5|10|30|60]  Time interval in minutes. time - interval
                                 [default: 10]
  -u, --unit [m|h|d]             Time unit for the time. can be min, hr, day
                                 [default: m]
  -f, --filter TEXT              Provide filters as attribute=value or
                                 attribute~value, the ~ will do regex
  -g, --groupby TEXT             Groupby criteria defining the nodes in the
                                 map e.g. pod_name, host_name, tags.kube_app,
                                 etc.
  --help                         Show this message and exit.
  ```
The create command has only one required parameter `name`. But to generate a meaningful map at least the group options should be leveraged. The groupby attributes can be provided using the `-g` option and they take values such as `pod_name`, `host_name` or tags such as `tags.kube_namespace`, `tags.kube_app`, etc. Multiple grouping attributes can be provided by repeating the `-g` option. The below example creates a service map defined by the `kube_app` label.
``` bash
>> netsil map create PodMap -g "pod_name" -f "tags.kube_namespace=sock-shop" -t 1 -u "h" -i 10
```
This command will create the map in Netsil as well as it will save a local copy in the `PodMap.map` file. The file essentially contains the nodes, edges and attributes used to create the map. This local map file can be used to analyze the structure of the distributed application. Before we look into some of the map analysis functions, it is important to understand how to pass the time parameters to create the map for a specific time window. Since Netsil uses UTC format, the easiest option to input time is by subtracting from `now`. If you want the map for a 10 min interval which was 1 hr ago, then simply provide `-t 1 -u h -i 10` i.e. 10min window, 1h ago.

# Analyzing Maps
``` bash
netsil map --help
Usage: netsil map [OPTIONS] COMMAND [ARGS]...

  Netsil AOC Map Commands

Options:
  --help  Show this message and exit.

Commands:
  create    Create Map & Save Locally In <Name.map> File
  delete    Delete the Map
  describe  Get Map Details
  edges     Get Edges For Nodes
  get       Get Map & Update Local Copy
  list      List All Maps
  paths     Get Paths From Source To Target Node
  tree      Get Traversal Tree From Source
  ```
The `describe`, `edges`, `paths` and `tree` command help analyze the structure of the distribute application. All these functions operate using the local copy of the map and hence just need the `Map Name` as input.
- `netsil map describe` : prints all the nodes and edges in the map. 
- `netsil map edges` : prints the "in", "out" or "all" the edges for the input list of nodes. 
- `netsil map paths` : prints all the paths between the input source and target node
- `netsil map tree` : print the edges resulting from depth-first or breadth-first traversal of the map

Example: Paths in the SockShop map between front-end and catalogue-db pod. There is a path that goes from `front-end --> catalogue --> catalogue-db`
``` bash
netsil map paths SockShop front-end catalogue-db
Paths
=====
[{'instance_type': 'container', 'pod_name': 'sock-shop/front-end-2337481689-l886j'}, {'instance_type': 'container', 'pod_name': 'sock-shop/catalogue-4293036822-dx87x'}, {'instance_type': 'container', 'pod_name': 'sock-shop/catalogue-db-1846494424-vjn2c'}]
```
# Get, List and Delete Map
These commands work on the `map id`. The `list` command can be used to obtain the map name and id. The `get` command will update the local copy of the map. 



