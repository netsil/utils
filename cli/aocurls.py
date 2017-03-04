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


#== Alert URLs ==
def GetAlertURL():
    return GetAOCURL()+"/api/v0/alert/instance"

def GetAlertDetailsURL():
    return GetAlertURL()

def GetAlertRuleURL():
    return GetAOCURL()+"/api/v0/alert/rule"

def GetAlertRuleDetailsURL():
    return GetAlertRuleURL()
