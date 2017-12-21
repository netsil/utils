import os

def GetCredentials():
    username = os.environ["AOC_USER"]
    password = os.environ["AOC_PWD"]
    payload = {
        'username': username,
        'password': password
    }
    return payload


def GetAOCURL():
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
