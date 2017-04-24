import requests
import random
import datetime

CHART_REQUEST_URL = "https://charturl.com/short-urls.json?api_key=%s"

def make_chart(data):
    API_KEY = "dak-b23c97b6-90eb-48bd-8ec2-e0ceb8c73fb4"
    #API_KEY= "pak-bdffc0a6-9164-4955-9513-ef7e26ed1e1e"
    
    labels=[]
    datapoints={}
    for item in data[data.keys()[0]]['data']:
        x=item[data[data.keys()[0]]['metadata']['columns'][1]]
        y=item[data[data.keys()[0]]['metadata']['columns'][0]]
        label=''
        if(len(data[data.keys()[0]]['metadata']['columns'])>2):
            for i in range(2,len(data[data.keys()[0]]['metadata']['columns'])):
                label=label+item[data[data.keys()[0]]['metadata']['columns'][i]]+' '
            label.strip()
        else:
            label="A"
        xx=datetime.datetime.fromtimestamp(int(x/1000)).strftime('%M:%S')
        if xx in labels:
            pass
        else:
            labels.append(xx)
        if(datapoints.has_key(label)):
            datapoints[label].append(y)
        else:
            datapoints[label]=[]
            datapoints[label].append(y)

    datasets=[]
    for key in datapoints.keys():
        d={}
        d["label"]=key
        d["data"]=datapoints[key]
        d["borderColor"]="rgba("+str(random.randint(0,255))+","+str(random.randint(0,255))+","+str(random.randint(0,255))+",1)"
        d["radius"]=0
        d["fill"]=False
        datasets.append(d)
    
    request_data = {
        'template': 'multi-line',
          "options" : {
            "data" : {
              "labels" : labels,
              "datasets" : datasets
            }
          }
        }


    request_url = CHART_REQUEST_URL % API_KEY
    #print 'making call to %s with %s' % (request_url, request_data)
    res = requests.post(request_url, json=request_data)
    if not res.ok:
        print 'request failed'
        print res.content

    chart_url = res.json()['short_url']

    response=[]
    attachmentItem = {}
    attachmentItem['fallback']=''
    #attachmentItem['pretext']=title
    attachmentItem['color']='#7CD197'
    attachmentItem['image_url']=chart_url
    response.append(attachmentItem)

    return response

    


