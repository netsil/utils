## Overview
The Netsil AOC CLI is a handy tool for operators to manage common tasks related to monitoring a distributed application. Below are some of the examples of tasks you can do efficiently with the CLI:
- Create, delete, update and mute alerts
- Create dashboards and add multiple charts to it
- Run a query to pull in specific metrics 
- Create a Netsil map and navigate it to understand dependencies 

## Dockerized Setup
You can run the CLI through docker as well.

First, build it with

```bash
$ TAG=<your-tag> ./docker-build.sh
```

The default tag is `netsil/cli`

Then, run it like so:

```bash
$ docker run -t netsil/cli
Usage: netsil [OPTIONS] COMMAND [ARGS]...

  Netsil AOC CLI

Options:
  --help  Show this message and exit.
...
```

## CLI Setup on Mac
Following steps have been tested on macOS 10.12
``` bash 
git clone https://github.com/netsil/utils.git   #clone netsil utils repo

cd /your_clone_of_netsil_utisl/cli    #change to the cli directory
 
sudo pip install virtualenv        #install virtualenv

virtualenv venv       #launch a virtual env in the cli/ folder

. venv/bin/activate   #Activate virtual env

source package.sh     #Install dependencies and netsil cli

export AOC_USER=<aoc_username>                          #(set your aoc username)
export AOC_PWD=<aoc_password>                          #(set your aoc password) 
export AOC_URL=https://your.netsil.url                 #(leave out the end '/')
```

``` bash
netsil --help     #All set if you see below message

(venv) $ netsil --help
Usage: netsil [OPTIONS] COMMAND [ARGS]...

  Netsil AOC CLI

Options:
  --help  Show this message and exit.

Commands:
  alert      Netsil AOC Alert Commands
  dashboard  Netsil AOC Dashboard Commands
  query      Netsil AOC Query Commands
  map        Netsil AOC Map Commands
```
## CLI Commands
Refer [docs](docs/) for more details on specific set of commands. 

[Alert](alert.md)
``` bash 
netsil alert --help
Usage: netsil alert [OPTIONS] COMMAND [ARGS]...

  Netsil AOC Alert Commands

Options:
  --help  Show this message and exit.

Commands:
  create  Create Alert
  delete  Delete Alert
  exp     Save Alerts To File
  get     Details for alert
  imp     Create Alerts From File
  list    List all alerts
  policy  Commands for alert policy
  update  Update Alert
  ```
[Dashboard](dashboard.md)
``` bash
netsil dashboard --help
Usage: netsil dashboard [OPTIONS] COMMAND [ARGS]...

  Netsil AOC Dashboard Commands

Options:
  --help  Show this message and exit.

Commands:
  addchart  Add Chart to Dashboard
  create    Create Dashboard
  delete    Delete Dashboard
  exp       Save Dashboards To File
  get       Get Dashboard
  imp       Create Dashboards From File
  list      List All Dashboards
```
 [Map](map.md)
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
[Query](ql.md)
``` bash
netsil query --help
Usage: netsil query [OPTIONS] COMMAND [ARGS]...

  Netsil AOC Query Commands

Options:
  --help  Show this message and exit.

Commands:
  run  Run Query
```
