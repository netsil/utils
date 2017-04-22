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
