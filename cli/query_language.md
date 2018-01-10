## Netsil CLI Query Language
The alert, dashboards and query commands rely on passing the query expression to define the metrics. CLI supports simple, prometheus style query expression. Below is an example of the query expression along with details of the syntax

`throughput(http.request_response.throughput {http.status_code=500, http.uri~"/orders"}) by (server.pod_name, client.pod_name) top(10)`
- `throughput` is the aggregation function
- `http.request_response.throughput` is the datasource
- `{ }` represents the filter clause
- `http.status_code = 500` is a matching filter
- `http.uri ~ "/orders"` is a regex for all `uri` container `/orders`
- `by (server.pod_name, client.pod_name)` is groupby operation on the list of attributes
- `top(10)` is the top function

So the core usage provides for 
- applying an aggregation function usually - avg, min, max, throughput, sum
- specifying the datasource such as - cpuUser, cpuSystem, http.request_response.latency
- specifying filters for either matching or regex
- grouping by a list of attributes
- top
Only aggregation function and datasource are required others are optional but used frequently.
`agg_func ( datasource { filter_key = filter_value, filter_key ~ filter_value, ... } ) by (attr1, attr2,...) top(X)`

Advanced usage also provides two additional operations in the query
- TimeRollup
- TimeShift
