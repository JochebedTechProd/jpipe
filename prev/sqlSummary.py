import mysql.connector
import json
import sys
def Average(lst): 
    return sum(lst) / len(lst)
param = sys.argv[1]
print(param)
deviceID = sys.argv[2]
minVal = sys.argv[3]
maxVal = sys.argv[4]
fromDate = sys.argv[5]
toDate = sys.argv[6]
funcType = sys.argv[7]
mydb = mysql.connector.connect(
host="localhost",
    user="jpipe",
      passwd="jpipe",
        database="JpipeDB")
#select * from JP_Device_Data where Change_Date > '2019-07-03 00:00' and Change_Date < '2019-07-04 10:00' where ;
def timeSummaryVal(param,deviceID,minVal,maxVal,fromDate,toDate):
    sqlStr = "SELECT Device_Data FROM JP_Device_Data WHERE Change_Date > '"+fromDate+"' and Change_Date < '"+toDate+"' and DeviceId = '"+deviceID+"'"
    print(sqlStr)
    mycursor = mydb.cursor()
    mycursor.execute(sqlStr)
    myresult = mycursor.fetchall()
    count =0
    for x in myresult:
        jsonStr = json.loads(x[0])
        if(float(jsonStr[param])>=float(minVal) and float(jsonStr[param])<float(maxVal)):
                        count = count+1
    print count*2
    return count*2
def averageVal(jsonStr):
    return jsonStr
def CheckFunc(funcToCheck,jsonData):
    global param,deviceID,minVal,maxVal,fromDate,toDate
    if(funcToCheck == 'timeSummaryVal'):
        retStr = timeSummaryVal(param,deviceID,minVal,maxVal,fromDate,toDate)
        return retStr
    elif(funcToCheck == 'averageVal'):
        mylist=[]
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Device_Data FROM JP_Device_Data")
        myresult = mycursor.fetchall()
        for x in myresult:
            print(x[0])
            jstring=x[0]
            g=json.loads(jstring)
            print(g['V'])
            mylist.append(float(g['V']))
        print(Average(mylist))
        retStr = averageVal(jsonData)
        return retStr
if(funcType=='timeSummaryVal'):
    print CheckFunc('timeSummaryVal','hello world')
elif(funcType=='averageVal'):
    print CheckFunc('averageVal','hello world')
