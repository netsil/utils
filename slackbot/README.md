# Netsil SlackBot

``` bash
export AOC_USER=<aoc_username>              #(set your aoc username)
export AOC_PWD=<aoc_password>              #(set your aoc password) 
export AOC_URL=https://your.netsil.url     #(leave out the end '/')
export AOC_SLACKBOT_NAME='netsilbot'		  #(set your slackbot name) 					
export AOC_SLACKBOT_TOKEN=<slackbot_token>	  #(set your slackbot token)
											  #For Netsil: Get token from https://netsil-inc.slack.com/apps/

```
``` bash
python netsilbot.py
```

``` bash
@netsilbot alert list
@netsilbot alert list text
@netsilbot alert list raw

@netsilbot alert details <alertID>

@netsilbot service list
@netsilbot service list text
@netsilbot service list raw

@netsilbot service details <serviceID>

@netsilbot alert rule list
@netsilbot alert rule list text
@netsilbot alert rule list raw

@netsilbot alert template list
@netsilbot alert template list text
@netsilbot alert template list raw

```

``` bash
Slackbot Query Format:
@netsilbot query run VariableName = Aggregation (DataSource {Filters}) by (GroupBys) top(N) timeshift time granularity time [timeInterval]

- Filters, GroupBys, timeshift, granularity and timeInterval are optional
- Filters can be match type (=) or regex type (~)
- Multiple filters and group-bys supported. Separate them by commas. 


Query Examples:
@netsilbot query run A = sum(http.request_response.latency)

@netsilbot query run A = avg ( http.request_response.latency {http.status.code=200} ) by (http.uri) top(5) timeshift 30s

@netsilbot query run A = avg ( http.request_response.latency {http.uri=/customers} ) by (http.request_method) top(5) timeshift 30s [10m]

@netsilbot query run A = throughput ( http.request_response.count {http.status.code=200} ) by (http.uri) top(5) [10m]

@netsilbot query run A = throughput ( http.request_response.count {http.status.code=200} ) by (http.uri) top(5)

@netsilbot query run A = avg ( mysql.request_response.latency {mysql.user=root} ) by (mysql.query) top(5) timeshift 30s

@netsilbot query run A = avg ( cassandra.request_response.latency {cassandra.error.code=Invalid} ) by (cassandra.query) top(5) timeshift 30s

@netsilbot query run A = avg ( http.request_response.latency {http.request_method=GET,http.status.code=200} ) by (http.uri) top(5) timeshift 30s

@netsilbot query run A = avg ( http.request_response.latency ) by (http.uri,http.request_method) top(5) [10m]

@netsilbot query run A = avg ( http.request_response.latency {http.status.code=200}) by (http.uri,http.request_method) top(10) timeshift 30s granularity 100s [10m]

@netsilbot query run A = avg ( mysql.request_response.latency {mysql.user=root} ) by (mysql.query) top(5) timeshift 30s [10m]

@netsilbot query run A = avg ( http.request_response.latency {http.status.code~4..}) by (http.request_method) top(10) timeshift 30s [10m]
```
