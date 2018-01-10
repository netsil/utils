## Alert Commands
Following commands are available for working with alerts
``` bash
>> netsil alert --help
Usage: netsil alert [OPTIONS] COMMAND [ARGS]...

  Netsil AOC Alert Commands

Options:
  --help  Show this message and exit.

Commands:
  create  Create Alert
  delete  Delete Alert
  get     Details for alert
  list    List all alerts
  policy  Commands for alert policy
  update  Update Alert

```
## Create Alert
``` bash
>> netsil alert create --help
Usage: netsil alert create [OPTIONS] NAME QUERY

  Create Alert

Options:
  -c, --critical FLOAT            Critical threshold
  -w, --warning FLOAT             Warning threshold
  -o, --operator [>|<|=]          Operator to check for threshold violation
                                  e.g. > critical threshold  [default: >]
  -d, --duration [1|5|10|30|60]   Time window to evaluate the alert, in mins
                                  [default: 1]
  -a, --aggregation [avg|max|min]
                                  Aggregation function to apply for metrics in
                                  time window  [default: avg]
  -p, --plot [line|area|stack-bar|bar|table|pie|gauge]
                                  Chart plot type  [default: line]
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
## Delete, Get, List and Update Alert
All these commands take the `alert id` as the input for manipulating the alert. 
- The `list` command can be used to get the name and id of the alerts. 
- The `update` command will update the attributes provided in the options including an option to mute/unmute alerts for e.g. during scheduled downtime.
``` bash
>> netsil alert update --help
Usage: netsil alert update [OPTIONS] ALERTID

  Update Alert

Options:
  -n, --name TEXT                 Name
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
  -m, --mute BOOLEAN              Mute/Unmute an alert
  --help                          Show this message and exit.

```
## Alert Policy
The alert policy command provide details on various notification policies configured in Netsil. Currently, `webhook`, `email` and `pagerduty` are the supported policy types. 
``` bash
netsil alert policy --help
Usage: netsil alert policy [OPTIONS] COMMAND [ARGS]...

  Commands for alert policy

Options:
  --help  Show this message and exit.

Commands:
  delete   Delete Alert Policy
  details  Details for alert policy
  list     List all alert policies
  ```
To associate a specific notification policy to an alert, you can simply do and then pass the policy id and policy type to the alert create option. For e.g.
``` bash
>> netsil alert policy list -t "webhook"
WebHook Alert Policies
id                                   	name                     	uri                           	
---------------------------------------------------------------------------------------------------------------
0e695c74-871a-4c97-801c-28f8a0ea96aa 	Zapier End To End Test   	https://hooks.zapier.com/hooks/catch/authstuff                          	
8c955b37-8a42-4703-be6c-5be5d06ed0d2 	SMB-Testing-Slack-Alerts 	https://hooks.slack.com/services/authstuff 	
---------------------------------------------------------------------------------------------------------------
2
```

