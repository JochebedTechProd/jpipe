import mysql.connector
import json
import sys
import datetime
#global mydb = None

############################################################################################################################
def callSnippet(callFunc,inData,dbParam):
    global mydb
    if (dbParam!=None):
        mydb=dbParam
    else:
        mydb = mysql.connector.connect(
            host="localhost",
            user="jpipe",
            passwd="jpipe",
            database="JpipeDB")
    global param,deviceID,minVal,maxVal,fromDate,toDate
    if(callFunc == 'fieldSummary'):
        retStr = fieldSummary(inData)
        return retStr
    elif(callFunc == 'graphData'):
        retStr = graphData(inData)
        return retStr
############################################################################################################################
def fieldSummary(inData):
    inJsonStr = json.loads(inData)
    # {"userid":"admin1","devId":"2","jsonStrKey":"V","fromDate":"2019-07-03 00:00","toDate":"2019-07-04 00:00","minVal":"0","maxVal":"12"}

    if (inJsonStr.get("userid")):
        userid = inJsonStr["userid"]
    else:
        retStr = '{"retCode":-404,"retDesc":"Missing user id-userid"}'
        return retStr

    #print(userid)
    if (inJsonStr.get("devId")):
        deviceID = inJsonStr["devId"]
    else:
        deviceID = -1

    if (inJsonStr.get("jsonStrKey")):
        jsonStrKey = inJsonStr["jsonStrKey"]
    else:
        retStr = '{"retCode":-404,"retDesc":"Missing JSON Key-jsonStrKey"}'
        return retStr

    if (inJsonStr.get("fromDate")):
        fromDate = inJsonStr["fromDate"]
    else:
        fromDate = "2001-01-01 00:00" #get all data from start as start date was not specified

    if (inJsonStr.get("toDate")):
        toDate = inJsonStr["toDate"]
    else:
        toDate = "2100-01-01 00:00" #get all data till now as end date was not specified

    if (inJsonStr.get("minVal")):
        minSearchVal = inJsonStr["minVal"]
    else:
        minSearchVal = -9999999999.0

    if (inJsonStr.get("maxVal")):
        maxSearchVal = inJsonStr["maxVal"]
    else:
        maxSearchVal = +9999999999.0

    sqlStr = "SELECT A.Device_Data, A.Change_Date FROM JP_Device_Data A,  JP_Users B WHERE username = '"+ userid+ "' and A.userid=B.userid and A.Change_Date > '"+fromDate+"' and A.Change_Date < '"+toDate+"'" 
    if (deviceID != -1):
       sqlStr += " and DeviceId = '"+deviceID+"' "
    sqlStr += " order by Change_Date desc"
        
    #print(sqlStr)
    mycursor = mydb.cursor()
    mycursor.execute(sqlStr)
    myresult = mycursor.fetchall()
    countVal =0
    minDataVal =None
    maxDataVal =None
    sumVal=0
    timeVal=None
    prevChangeDtFrmt=None
    for currRow in myresult:
        dataJsonStr = json.loads(currRow[0])
        #print (dataJsonStr)
        #print (currRow[1])
        currChangeDate = str(currRow[1])
        currChangeDtFrmt = datetime.datetime.strptime(currChangeDate, '%Y-%m-%d %H:%M:%S')
        #print('Time:', currChangeDtFrmt.time())
        if (not (dataJsonStr.get(jsonStrKey))):
            continue  #value requested is not present in data so ignore it
        valueOfVariable=float(dataJsonStr[jsonStrKey])
        if(valueOfVariable>=float(minSearchVal) and valueOfVariable<=float(maxSearchVal)):
            countVal = countVal+1
            sumVal += valueOfVariable
            if (minDataVal==None):
                minDataVal=valueOfVariable
                maxDataVal=valueOfVariable
            if (valueOfVariable<minDataVal):
                minDataVal=valueOfVariable
            if (valueOfVariable>maxDataVal):
                maxDataVal=valueOfVariable
            if (prevChangeDtFrmt != None):
                if (timeVal!=None):
                    #print "timeVal="+str(timeVal)
                    timeVal = timeVal + prevChangeDtFrmt - currChangeDtFrmt
                else:
                    timeVal = currChangeDtFrmt
                    timeVal = prevChangeDtFrmt - currChangeDtFrmt
        prevChangeDtFrmt = currChangeDtFrmt
    if (countVal>0):
        avgVal=float(sumVal/countVal)
    else:
        avgVal=None
    retStr = '{"retCode":0,"retDesc":"data returned","data":{"count":'+str(countVal)+',"sum":'+str(sumVal)+',"avg":'+str(avgVal)+',"min":'+str(minDataVal)+',"max":'+str(maxDataVal)+',"timeWithVal":'+str(timeVal)+'}}'
    print retStr
    return retStr
############################################################################################################################
def graphData(inData):
    inJsonStr = json.loads(inData)
    # {"userid":"admin1","devId":"2","jsonStrKey":["V","charge"],"fromDate":"2019-07-03 00:00","toDate":"2019-07-04 00:00","typt":"normal"}         
    #type values - cummulative

    if (inJsonStr.get("userid")):
        userid = inJsonStr["userid"]
    else:
        retStr = '{"retCode":-404,"retDesc":"Missing user id-userid"}'
        return retStr

    if (inJsonStr.get("devId")):
        deviceID = inJsonStr["devId"]
    else:
        deviceID = -1

    if (inJsonStr.get("jsonStrKey")):
        jsonStrKey = inJsonStr["jsonStrKey"]
        print jsonStrKey
        jsonStrKeyLen = len(inJsonStr["jsonStrKey"])
        print "jsonStrKeyLen="+str(jsonStrKeyLen)
    else:
        retStr = '{"retCode":-404,"retDesc":"Missing JSON Key-jsonStrKey"}'
        return retStr

    if (inJsonStr.get("fromDate")):
        fromDate = inJsonStr["fromDate"]
    else:
        fromDate = "2001-01-01 00:00" #get all data from start as start date was not specified

    if (inJsonStr.get("toDate")):
        toDate = inJsonStr["toDate"]
    else:
        toDate = "2100-01-01 00:00" #get all data till now as end date was not specified

    sqlStr = "SELECT A.Device_Data, A.Change_Date FROM JP_Device_Data A,  JP_Users B WHERE username = '"+ userid+ "' and A.userid=B.userid and A.Change_Date > '"+fromDate+"' and A.Change_Date < '"+toDate+"'" 
    if (deviceID != -1):
       sqlStr += " and DeviceId = '"+deviceID+"' "
    sqlStr += " order by Change_Date desc"
        
    print(sqlStr)
    mycursor = mydb.cursor()
    mycursor.execute(sqlStr)
    myresult = mycursor.fetchall()
    print "rows returned = "+str(len(myresult))
    countVal =0
    retStr = '{"retCode":0,"retDesc":"data returned","data":['
    firstRowData=True
    for currRow in myresult:
        if (firstRowData):
            firstRowData=False
        else:
            retStr+=','
        dataJsonStr = json.loads(currRow[0])
        #print (dataJsonStr)
        #print (currRow[1])
        currChangeDate = str(currRow[1])
        currChangeDtFrmt = datetime.datetime.strptime(currChangeDate, '%Y-%m-%d %H:%M:%S')
        retStr+='{"time":"'+currChangeDate+'","rowData":{'
        #print('Time:', currChangeDtFrmt.time())
        firstFieldData=True
        for searchJsonKey in jsonStrKey:
            #print searchJsonKey+"="+dataJsonStr[searchJsonKey]
            if (firstFieldData):
                firstFieldData = False
            else:
                retStr+=','
            if (dataJsonStr.get(searchJsonKey)):
                retStr+='"'+searchJsonKey+'":"'+dataJsonStr[searchJsonKey]+'"'
            else:
                retStr+='"'+searchJsonKey+'":"None"'
        retStr+='}'
        #print retStr
    retStr += '}'
    print retStr
    return retStr
############################################################################################################################
