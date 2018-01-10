## Managing Dashboards
You can fully manage dashboards from the cli starting by creating dashboards and adding multiple charts to them.
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
  get       Get Dashboard
  list      List All Dashboards
  ```
## Creating Dashboard and Adding Charts
Creating dashboard is simple and just requires name of the dashboard. Adding chart to the dashboard takes the `dashboard id` and query expression for the chart. Multiple query expressions can be passed to create a chart of multiple metrics. 

``` bash
netsil dashboard addchart --help
Usage: netsil dashboard addchart [OPTIONS] DASHBOARD_ID NAME [QUERY]...

  Add Chart to Dashboard

Options:
  -p, --plot [line|area|stack-bar|bar|table|pie|gauge]
                                  Chart plot type  [default: line]
  --help                          Show this message and exit.
  ```
 Example: Adding a chart named "CPU Chart" that plots both cpuSystem and cpuUser plots
 ``` bash
 >> netsil dashboard addchart 4920bfe7-2d86-4258-9821-3b3f040f60c2 "CPU Chart" "avg(cpuUser) by (instance.host_name)" "avg(cpuSystem) by (instance.host_name)"
```
Note: refer [Query Language](ql.md) for more details on the query expression.

## Delete, Get and List Dashboards
These commands use the `dashboard id` to manipulate the specific dashboard. The `id` can be obtained by using the `list` command.
