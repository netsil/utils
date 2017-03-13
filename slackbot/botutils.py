import json

def PrettyResponseTable(arrayOfObjects, keys = [], title=''):
    response=[]
    printWidth= {}
    if len(arrayOfObjects) <= 0:
        return
    if len(keys) == 0:
        keys = arrayOfObjects[0].keys()
    
    index=0
    for obj in arrayOfObjects:        
        attachmentItem = {}
        attachmentItem['fallback']=''
        if(index==0):
            attachmentItem['pretext']=title

        if(index%2==0):            
            attachmentItem['color']='#7CD197'
        else:
            attachmentItem['color']='#F35A00'

        attachmentItem['fields']=[]
        for key in keys:
            field={}
            field['title']=str(key)
            field['value']=str(obj[key])
            field['short']=False
            attachmentItem['fields'].append(field)
        response.append(attachmentItem)
        index=index+1
    
    return response

def PrettyResponseText(arrayOfObjects, keys = []):
    response=''
    printWidth= {}
    if len(arrayOfObjects) <= 0:
        return
    if len(keys) == 0:
        keys = arrayOfObjects[0].keys()

    dashCount = 2
    for key in keys:
        printWidth[key]= max(len(key), max(len(str(obj[key])) for obj in arrayOfObjects))
        dashCount = dashCount + printWidth[key]+ 6

    dashline = "-" * dashCount
    keyString = ""
    for key in keys:
        keyString = keyString + "%s \t" % str(key).ljust(printWidth[key])

    response += keyString + '\n'
    response += dashline + '\n'
    for obj in arrayOfObjects:
        rowString = ""
        for key in keys:
            rowString = rowString + "%s \t" % str(obj[key]).ljust(printWidth[key])
        response += rowString + '\n'

    response += dashline + '\n'
    response += str(len(arrayOfObjects))+'\n'
    return response

def PrettyPrint(arrayOfObjects, keys = []):
    printWidth= {}
    if len(arrayOfObjects) <= 0:
        return
    if len(keys) == 0:
        keys = arrayOfObjects[0].keys()

    dashCount = 2
    for key in keys:
        printWidth[key]= max(len(key), max(len(str(obj[key])) for obj in arrayOfObjects))
        dashCount = dashCount + printWidth[key]+ 6

    dashline = "-" * dashCount
    keyString = ""
    for key in keys:
        keyString = keyString + "%s \t" % str(key).ljust(printWidth[key])

    print keyString
    print dashline
    for obj in arrayOfObjects:
        rowString = ""
        for key in keys:
            rowString = rowString + "%s \t" % str(obj[key]).ljust(printWidth[key])
        print rowString

    print dashline
    print len(arrayOfObjects)
    return
    
def JSONLoadsString(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data
    
