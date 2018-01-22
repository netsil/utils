import os
import sys

DEFAULT_AOC_URL = "https://prod-cloud.netsil.com"

def GetCredentials():
    if "AOC_USER" not in os.environ or "AOC_PWD" not in os.environ:
        print "Need to set AOC_USER and AOC_PWD" 
        sys.exit(1)

    username = os.environ["AOC_USER"]
    password = os.environ["AOC_PWD"]
    payload = {
        'username': username,
        'password': password
    }
    return payload


def GetAOCURL():
    if "AOC_URL" not in os.environ:
        return DEFAULT_AOC_URL
    return os.environ["AOC_URL"]

def GetAuthURL():
    return GetAOCURL()+"/login"

#== Service URLs ==
def GetServiceURL():
    return GetAOCURL()+"/api/v0/service"

def GetServiceDetailsURL():
    return GetServiceURL()

#== Alert Template URLs ==
def GetAlertTemplateURL():
    return GetAOCURL()+"/api/v0/alert/template"

def GetAlertTemplateDetailsURL():
    return GetAlertTemplateURL()

def GetAlertTemplateCreateURL():
    return GetAlertTemplateURL()


#== Alert URLs ==
def GetAlertURL():
    return GetAOCURL()+"/api/v0/alert"

def GetAlertDetailsURL():
    return GetAlertURL()

def GetAlertCreateURL():
    return GetAlertURL()
            
def GetAlertRuleURL():
    return GetAOCURL()+"/api/v0/alert/rule"

def GetAlertRuleDetailsURL():
    return GetAlertRuleURL()

def GetAlertRuleCreateURL():
    return GetAlertRuleURL()

def GetAlertTriggerURL():
    return GetAOCURL()+"/api/v0/alert/trigger"

def GetAlertTriggerCreateURL():
    return GetAlertTriggerURL()

def GetAlertNotificationURL(ptype):
    return GetAOCURL() + "/api/v0/alert/notification/" + ptype

def GetAlertPolicyURL(ptype):
    return GetAOCURL() + "/api/v0/alert/policy/" + ptype

#== Query URLs ==
def GetQueryPostURL():
    return GetAOCURL()+"/query/analytics"

#== Dashboard URLs ==
def GetDashboardURL():
    return GetAOCURL()+"/dashboards"

#== Map URLs ==
def GetMapURL():
    return GetAOCURL()+"/topology/services"

def GetTopologyMapURL():
    return GetAOCURL()+"/auth-api/topology-map"
