import os

def GetCredentials():
    username = os.environ["AOCUSER"]
    password = os.environ["AOCPWD"]
    payload = {
        'username': username,
        'password': password
    }
    return payload


def GetAOCURL():
    return os.environ["AOCURL"]

def GetAuthURL():
    return GetAOCURL()+"/login"

#== Service URLs ==
def GetServiceURL():
    return GetAOCURL()+"/api/v0/service"

def GetServiceDetailsURL():
    return GetServiceURL()

#== Alert Template URLs ==
def GetAlertTemplateURL():
    return GetAOCURL()+"/api/v0/alert"

def GetAlertTemplateDetailsURL():
    return GetAlertTemplateURL()


#== Alert URLs ==
def GetAlertURL():
    return GetAOCURL()+"/api/v0/alert/instance"

def GetAlertDetailsURL():
    return GetAlertURL()


