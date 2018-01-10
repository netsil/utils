## Querying Netsil Time Series Database
Most of the time dashboards, charts and alerts are required to understand the time series metrics. But often there are scenarios where a simple metric such as `avg disk usage` or `container count on the host` might be useful from the cli. The `netsil query` command can be used for such simple metrics scenario. For more complex metrics handling, please check out the [dashboard and charting](dashboard.md) commands.
``` bash
netsil query run --help
Usage: netsil query run [OPTIONS] QUERY

  Run Query

Options:
  -f, --filename
  -s, --start INTEGER        start time for query specified as (now - s)
                             [default: 300]
  -e, --end INTEGER          end time for query specified as (now - e)
                             [default: 0]
  -u, --unit [s|m|h|d]       time unit for the interval and granularity
                             [default: s]
  -g, --granularity INTEGER  granularity of data  [default: 60]
  --help                     Show this message and exit.
  ```
  Note: refer to [Query Language](ql.md) for details on the query expression syntax

