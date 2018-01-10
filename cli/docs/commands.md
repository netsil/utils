## Managing Alerts
``` bash
>> netsil alert create --help
Usage: netsil alert create [OPTIONS] NAME QUERY

  Create Alert

Options:
  -c, --critical FLOAT            Critical threshold
  -w, --warning FLOAT             Warning threshold
  -o, --operator [>|<|=]          Operator to check for threshold violation
                                  e.g. > critical threshold
  -d, --duration [1|5|10|30|60]   Time window to evaluate the alert, in mins
  -a, --aggregation [avg|max|min]
                                  Aggregation function to apply for metrics in
                                  time window
  -p, --plot [line|area|stack-bar|bar|table|pie|gauge]
                                  Chart plot type
  -t, --policy_type [webhook|email|pagerduty]
                                  Notification policy type. Check out alert
                                  policy list for more details
  -i, --policy_id TEXT            Notification policy id. Check out alert
                                  policy list for more details
  --help                          Show this message and exit.
```
Example: Create an alert on available useable memory by host if it drops below 10%. Below is the name of the alert, query expression, and uses options `-c` for critical threshold, `-o` to define the operator as less than, `-a` for providing the aggregation function and `-d` to set the duration for evaluating the alert. 

``` bash
>> netsil alert create "MemorySpike" "avg(memPhysPctUsable) by (instance.host_name)" -c 10 -o "<" -a avg -d 5 
```
