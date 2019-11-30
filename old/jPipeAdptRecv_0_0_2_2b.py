import paho.mqtt.client as mqttClient
import AES_B64
import time
import uuid
import json
import random
import os
import web
from _mysql_exceptions import Warning, Error, InterfaceError, DataError, \
    DatabaseError, OperationalError, IntegrityError, InternalError, \
    NotSupportedError, ProgrammingError

# joins elements of getnode() after each 2 digits.
global glb_clientConnected
global glb_dataSubscribed
global glb_jpipeBaseDir
global glb_lastRecvConfigParms
glb_jpipeBaseDir = "."

print ("The MAC address in formatted way is : ")
print (''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                 for ele in range(0, 8 * 6, 8)][::-1]))
macAd=''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                 for ele in range(0, 8 * 6, 8)][::-1])
CLIENT_ID_REG=1
devReg=False
devRegSubTopic = "jts/jpipe/v000001/adapter/"+str(CLIENT_ID_REG)
print(devRegSubTopic)

cipher = AES_B64.AESCipher('0000000000000001')
glb_lastRecvConfigParms=""
#######################################################################################
def reqConfigDetails():
    global glb_inpParmLastCheckTime
    global glb_inpParmLastCheckInt
    if ( time.time()>glb_inpParmLastCheckTime):
        glb_inpParmLastCheckTime= time.time() + glb_inpParmLastCheckInt

        toLoad = '{"key":"1"}'
        toPublish = cipher.encrypt(str(toLoad))
        #print "toLoad=",toLoad,"="
        print "Pubishing data to =jts/jpipe/v000001/adapter/adapter_config="
        client.publish('jts/jpipe/v000001/adapter/adapter_config',toPublish)


#######################################################################################
def setupInboundTransmission():
    global glb_jpipeBaseDir
    global glb_lastRecvConfigParms
    #print "glb_lastRecvConfigParms=",glb_lastRecvConfigParms
    var_forwardType=str(glb_lastRecvConfigParms["Settings"]["forwardType"])
    if (var_forwardType=="ff"):
        var_inDir=str(glb_lastRecvConfigParms['Settings']['input_folder'])
        var_outDir=str(glb_lastRecvConfigParms['Settings']['output_folder'])
        var_inDir=var_inDir.replace("<base>",glb_jpipeBaseDir);
        var_outDir=var_outDir.replace("<base>",glb_jpipeBaseDir);

        if (not(os.path.isdir(var_inDir))):
            os.mkdir(var_inDir)
        if (not(os.path.isdir(var_outDir))):
            os.mkdir(var_outDir)
        var_tempDir = var_inDir+"/.store"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)
        var_tempDir = var_inDir+"/.store"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)
        var_tempDir = var_outDir+"/.store"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)
        var_tempDir = var_inDir+"/.store/stage"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)
        var_tempDir = var_inDir+"/.store/processed"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)
        var_tempDir = var_outDir+"/.store/stage"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)
        var_tempDir = var_outDir+"/.store/ackDue"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)
        var_tempDir = var_outDir+"/.store/processed"
        if (not(os.path.isdir(var_tempDir))):
            os.mkdir(var_tempDir)

    if (var_forwardType=="db"):
        var_dbType="mysql"
        var_dbServer=str(glb_lastRecvConfigParms['Settings']['dbServer'])
        var_dbName=str(glb_lastRecvConfigParms['Settings']['dbName'])
        var_dbUserId=str(glb_lastRecvConfigParms['Settings']['dbUserId'])
        var_dbPassword=str(glb_lastRecvConfigParms['Settings']['dbPassword'])
        #print var_dbType,var_dbServer,var_dbName,var_dbUserId,var_dbPassword
        try:
            db_handle = web.database(dbn=var_dbType, host=var_dbServer, db=var_dbName, user=var_dbUserId, pw=var_dbPassword)
            txn = db_handle.transaction()
            execQuery="create table inData(\
                dataId integer NOT NULL AUTO_INCREMENT,\
                transId integer, \
                macId varchar(12),\
                pins varchar(32),\
                data varchar(256),\
                status char(3) default 'rec',\
                ackSent boolean default False, \
                inserrtDt timestamp default current_timestamp, \
                changeDt timestamp default current_timestamp,\
                insertUser char(30) default 'application', \
                updateUser char(30) default 'application',\
                PRIMARY KEY (dataId),\
                CONSTRAINT UC_Person UNIQUE (transId))"
            #print "query=",execQuery
            results = db_handle.query(execQuery)
        except DatabaseError as(errno,strerror):
            if (errno==1054):
                print "Table inData already exists"
            else:
                ins_err="ERROR:"+"last_update_error-DatabaseError({0}):{1}".format(errno,strerror)
                print(ins_err)
        try:
            execQuery="create table outData(\
                dataId integer NOT NULL AUTO_INCREMENT,\
                transId integer, \
                macId varchar(12),\
                pins varchar(32),\
                data varchar(256),\
                status char(3) default 'rec',\
                ackSent boolean default False, \
                inserrtDt timestamp default current_timestamp, \
                changeDt timestamp default current_timestamp,\
                insertUser char(30) default 'application', \
                updateUser char(30) default 'application',\
                PRIMARY KEY (dataId),\
                CONSTRAINT UC_Person UNIQUE (transId))"
            #print "query=",execQuery
            results = db_handle.query(execQuery)
        except DatabaseError as(errno,strerror):
            if (errno==1054):
                print "Table outTable already exists"
            else:
                ins_err="ERROR:"+"last_update_error-DatabaseError({0}):{1}".format(errno,strerror)
                print(ins_err)


#######################################################################################
def processData(parm_allData,var_transId):
    global glb_jpipeBaseDir
    global glb_lastRecvConfigParms
    #print "data recv=",parm_allData
    #print "glb_lastRecvConfigParms=",glb_lastRecvConfigParms
    var_forwardType=str(glb_lastRecvConfigParms["Settings"]["forwardType"])
    for var_lineData in parm_allData:
        print var_lineData
        if (var_forwardType=="ff"):
            var_inDir=str(glb_lastRecvConfigParms['Settings']['input_folder'])
            var_outDir=str(glb_lastRecvConfigParms['Settings']['output_folder'])
            var_inDir=var_inDir.replace("<base>",glb_jpipeBaseDir);
            var_outDir=var_outDir.replace("<base>",glb_jpipeBaseDir);
            fileName="inData_"+str(var_transId)+"."+str(int(time.time()%10000000))
            print fileName

        elif (var_forwardType=="db"):
            var_dbType="mysql"
            var_dbServer=str(glb_lastRecvConfigParms['Settings']['dbServer'])
            var_dbName=str(glb_lastRecvConfigParms['Settings']['dbName'])
            var_dbUserId=str(glb_lastRecvConfigParms['Settings']['dbUserId'])
            var_dbPassword=str(glb_lastRecvConfigParms['Settings']['dbPassword'])
            #print var_dbType,var_dbServer,var_dbName,var_dbUserId,var_dbPassword
            #var_lineJsonData=json.loads(var_lineData)
            var_lineJsonData=var_lineData
            var_data=json.dumps(var_lineJsonData)
            var_pins=json.dumps(var_lineJsonData['pins'])
            if (var_transId <100):
                var_transId=int(time.time())
            try:
                db_handle = web.database(dbn=var_dbType, host=var_dbServer, db=var_dbName, user=var_dbUserId, pw=var_dbPassword)
                txn = db_handle.transaction()
                trans_id=db_handle.insert('inData',transId=var_transId,pins=var_pins,data=var_data,insertUser=var_dbUserId,updateUser=var_dbUserId)
                txn.commit()
            except DatabaseError as(errno,strerror):
                ins_err="ERROR:"+"last_update_error-DatabaseError({0}):{1}".format(errno,strerror)
                txn.rollback()
                print(ins_err)

#######################################################################################
def on_connect(client,user_data,flags,rc):
    print("connected with result code"+str(rc))
    client.subscribe(devRegSubTopic)

######################################################################################
def on_message(client,userdata,msg):
    global glb_lastRecvConfigParms
    global glb_inpParmLastCheckTime
    global glb_inpParmLastCheckInt

    #print msg.topic+str(msg.payload)
    #print msg.topic

    strToDecode = msg.payload
    appendText = cipher.decrypt(str(strToDecode))
    tempText=appendText.replace('\\\"','\"')
    replText=tempText.replace('\'','\"')
    #print "data=",replText
    try:
        inpData = json.loads(replText)
    except ValueError:
        print "\n\nInvalid input,no proper json request,not processing the data. \ninpData=",replText,"="
        return
    configRecv=False
    if('Settings' in inpData):
        if('forwardType' in inpData["Settings"]):
            configRecv=True
    #print "inpData=",inpData,"configRecv=",configRecv
    #------------- config params-----------------
    if (configRecv):
        print "config data received"
        glb_inpParmLastCheckTime= time.time() + glb_inpParmLastCheckInt
        if (glb_lastRecvConfigParms!=inpData):
            print "config data changed. writing data to config file"
            glb_lastRecvConfigParms=inpData
            if (not(os.path.isdir("config"))):
                os.mkdir("config")
            file1 = open("config/configFile.txt","w+")
            file1.write(replText)
            file1.close()
            setupInboundTransmission()
        return
    #------------- Data ----------------------------
    var_dataType=None
    if('dataType' in inpData):
        var_dataType=str(inpData['dataType'])
    if (var_dataType==None):
        print "Invalid input,no proper json request,not processing the data. Data=",inpData,"="
        return
    #------------- cld to Adpt data -----------------
    if (var_dataType=="c2a"):
        var_allData=inpData['data']
        var_transId=inpData['transId']
        processData(var_allData,var_transId)
        reqConfigDetails()
        return
    else:
        print "Input does not contain valid data. Ignoring data. Data=",inpData,"="
        return

######################################################################################
startTime = time.time()
glb_inpParmLastCheckTime = time.time()
glb_inpParmLastCheckInt = 10

fileConfig=None
configText = None
try:
    fileConfig = open("config/configFile.txt","r+")
    print "file config/configFile.txt opened"
    configText = fileConfig.readline()
    fileConfig.close()
    #print "config params read=",configText,"="
    print "config params already present. using them."
except :
    glb_lastRecvConfigParms = None
    print "params not present"
finally:
    if (fileConfig!=None):
        fileConfig.close()
if (configText!=None):
    glb_lastRecvConfigParms = json.loads(configText)
    setupInboundTransmission()

client=mqttClient.Client()
client.on_connect=on_connect
client.on_message=on_message

client.username_pw_set(username="esp", password="ptlesp01")
#client.connect("localhost", 1883, 60)
client.connect("cld003.jts-prod.in", 1883, 60)

client.loop_forever()
