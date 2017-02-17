def PrettyPrint(arrayOfObjects, keys):
    printWidth= {}
    for key in keys:
        printWidth[key]= max(len(str(obj[key])) for obj in arrayOfObjects)

    dashline = "-----------------------------------------------------------------------------"
    keyString = ""
    for key in keys:
        keyString = keyString + "%s \t" % str(key).ljust(printWidth[key])

    print keyString
    print dashline
    for obj in arrayOfObjects:
        rowString = ""
        for key in keys:
            # if obj[key] == None:
            #    rowString = rowString + "%s \t" % str(obj[key])
            # else:
            
            rowString = rowString + "%s \t" % str(obj[key]).ljust(printWidth[key])
        print rowString

    print dashline
    print len(arrayOfObjects)
    return
    

    
