
def FilterReader(filter):
    if "type" not in filter.keys():
        return None

    if filter["type"] == "match":
        return ("( " + filter["column"] + " = " + filter["value"]["text"] + " )" )
    if filter["type"] == "regex":
        return ("( " + filter["column"] + " regex " + filter["value"]["text"] + " )")
    if filter["type"] == "isin":
        return ("( " + filter["column"] + " isin " + filter["value"]["list"]["data"]["name"] + " )")
    
    filterString = filter["type"] + "( " 
    for field in filter["fields"]:
        filterString = filterString + " " + FilterReader(field)
    return filterString + " )"


def GroupByReader(groupby):
    groupbyString =" "
    for key in groupby.keys():
        if "SERIES" in key:
            groupbyString = groupbyString + " " + groupby[key]
    return groupbyString

def TopReader(top):
    return ("Top " + str(top["value"]) + " by " + top["column"])

def ExpressionReader(queryStatement):
    if "name" not in queryStatement.keys():
        return None

    dataframe = None
   
    if "value" in queryStatement.keys():
        if "dataframe" in queryStatement["value"].keys():
            dataframe = queryStatement["value"]["dataframe"]

    if dataframe == None:
        return None


    if "expr" in dataframe.keys():
        exprObject = {}
        exprObject["name"]  = queryStatement["name"]
        exprObject["expression"] = dataframe["expr"]
        return exprObject

    if "_type" in dataframe.keys():
        if dataframe["_type"] == "rolling":
            exprObject = {}
            exprObject["name"]  = queryStatement["name"]
            exprObject["expression"] = dataframe["_type"] + " " + dataframe["aggregation"] + " " + dataframe["window"] + " " + dataframe["dataframe"]["name"]
            return exprObject
        if dataframe["_type"] == "topn":
            exprObject = {}
            exprObject["name"]  = queryStatement["name"]
            ascending = "descending"
            if "ascending" in dataframe.keys():
                ascending = "ascending"
            exprObject["expression"] = dataframe["_type"] + " " + str(dataframe["n"]) + " " + dataframe["aggregation"] + " " + dataframe["dataframe"]["name"] + " (" + ascending + ")"
            return exprObject
    
    return None



def QueryReader(query):
    filter = "FILTER"
    top = "LIMIT"
    datasource = "report-name"
    groupby = "GroupBy"
    timeshift = "timeshift"
    function = "Metrics"
    aggregate = "aggregate"
    serviceFilter = "ServiceID"
    
    outDataSource = "datasource"
    outFunction = "aggregate"
    outGroupBy = "groupby"
    outFilter = "filter"
    outServiceFilter = "service"
    outTop = "top"
    outName = "name"
    outStatementRef = "statement"
    outTimeShift = "timeshift"
    outExpression = "expression"
    queryName = query["name"]
    queryObjects = []
    exprObjects = []
    for queryStatement in query["value"]["statements"]:
        if "name" not in queryStatement.keys():
            continue
        if "query" not in queryStatement["value"].keys():
            exprObject = ExpressionReader(queryStatement)
            if exprObject != None:
                exprObjects.append(exprObject)
            continue
        
        statementRef = queryStatement["name"]
        innerQuery = queryStatement["value"]["query"]
        queryOptions = innerQuery["options"]

        queryObject = {}
        queryObject[outName] = queryName
        queryObject[outStatementRef] = statementRef
        queryObject[outDataSource] = innerQuery[datasource]
        queryObject[outFunction] = queryOptions[function][statementRef][aggregate] 
        queryObject[outFilter] = FilterReader(queryOptions[filter])
        queryObject[outGroupBy] = GroupByReader(queryOptions[groupby])
        queryObject[outTimeShift] = queryOptions[timeshift]

        if top in queryOptions.keys():
            queryObject[outTop] = TopReader(queryOptions[top])
        else:
            queryObject[outTop] = None

        if serviceFilter in queryOptions.keys():
            queryObject[outServiceFilter] = queryOptions[serviceFilter]["server"]
        else:
            queryObject[outServiceFilter] = None
        queryObjects.append(queryObject)

    returnObjects = {}
    returnObjects["queries"] = queryObjects
    returnObjects["expressions"] = exprObjects
    return returnObjects

        




