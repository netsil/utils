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
- applying an aggregation function usually `avg`, `min`, `max`, `throughput`, `sum`, `count`, `rate`, etc.
- specifying the datasource such as `cpuUser`, `cpuSystem`, `memPhysFree`, `http.request_response.latency`, etc.
- specifying filters for either matching or regex
- grouping by a list of attributes
- top
Only aggregation function and datasource are required others are optional but used frequently. The grammar syntax looks like:

`agggreation_func ( datasource { filter_key = filter_value, filter_key ~ filter_value, ... } ) by (attr1, attr2,...) top(X)`

Advanced usage also provides two additional operations in the query
- TimeRollup : Often the granularity of collection is different from the granularity of quering. For e.g., `cpuSystem` might be collected at 1 sec granularity but in a query might need to be reported at 1 min granularity. In such cases, TimeRollUp provides the aggregation function to apply on the time bucket. So in the example, you could say TimeRollUp as `max` reported value in the 1min bucket. Note that there could potentially be 60 datapoints in that bucket. So an aggregation function is needed to "summarize" those points for the coarse granularity. 
The value of TimeRollup is an aggregation function such as `avg`,`max`, `min`, `sum`, etc. Most commonly `avg` is used as TimeRollup function. Below is the syntax to specify TimeRollup function.

agggreation_func ( datasource { filters } `[TimeRollup_func]` ) by (attr1, attr2,...) top(X)


- TimeShift : A timeshift by X mins will plot the datapoint from t-X at t. That is, it will plot the data points from X mins ago to the current time. This is particularly useful for comparing metrics across time. For e.g. comparing HTTP latency now vs 1 hour ago during an incident response.
TimeShift value is specified as number followd by `[s|m|h|d|w]` for seconds, mins, hrs, days, weeks. For e.g `1h` would be 1 hour time shift. The syntax for specifying TimeShift is below i.e. with keyword `offset`.

agggreation_func ( datasource { filters } [TimeRollup_func] ) by (attr1, attr2,...) top(X) `offset (1h)`

## Example Queries
- `avg(cpuSystem) by (instance.host_name)`
- `avg(http.request_response.latency { http.status_code = 200 }) by (client.pod_name) top (50)`
- `avg(http.request_response.latency { http.status_code = 200 }) by (client.pod_name) top (50) offset (1h)`
- `sum(docker.containers.running [avg]) by (instance.host_name)` Get count of running containers per host. Note the use of TimeRollup function since the collection of running containers per host could be at much granular level then the query time window.

