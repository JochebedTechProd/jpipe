import AES_B64
import paho.mqtt.client as mqttClient
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
global glb_mqttConnected
global glb_dataSubscribed
global glb_jpipeBaseDir
global glb_lastRecvConfigParms
glb_jpipeBaseDir = "."

print ("The MAC address in formatted way is : ")
print((''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                 for ele in range(0, 8 * 6, 8)][::-1])))
macAd=''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                 for ele in range(0, 8 * 6, 8)][::-1])
CLIENT_ID_REG=1
devReg=False
devRegPubTopic = "jts/jpipe/v000001/adaptorRegPub"
devRegSubTopic = "jts/jpipe/v000001/adapter/"+str(CLIENT_ID_REG)
print(devRegSubTopic)
subTopic = "jts/jpipe/v000001/adaptor/"+str(CLIENT_ID_REG)
devPubTopic = "jts/"
cipher = AES_B64.AESCipher('1234567812345668')
cipher = AES_B64.AESCipher('0000000000000001')
glb_lastRecvConfigParms=""
#######################################################################################
def reqConfigDetails():
    toLoad = '{"key":"1"}'
    toPublish = cipher.encrypt(str(toLoad))
    #print "toLoad=",toLoad,"="
    print("Pubishing data to =jts/jpipe/v000001/adapter/adapter_config=")
    client.publish('jts/jpipe/v000001/adapter/adapter_config',toPublish)

#######################################################################################
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")
#######################################################################################
def on_message(client, userdata, message):
    print(("Message received: "  + message.payload))

################### Main #################

broker_address = "cld003.jts-prod.in"  # Broker address
var_port = 1883  # Broker port
var_user = "esp"  # Connection username
var_password = "ptlesp01"  # Connection password

client = mqttClient.Client("Python")  # create new instance
client.username_pw_set(var_user, var_password)  # set username and password
client.on_connect = on_connect  # attach function to callback
#client.on_message = on_message  # attach function to callback
client.connect(broker_address, var_port,60)  # connect to broker

startTime = time.time()
inpParmLastCheckTime = time.time()
inpParmLastCheckInt = 2

while (1):  
    client.loop()
    if ( time.time()>inpParmLastCheckTime):
        inpParmLastCheckTime= time.time() + inpParmLastCheckInt
        elapsedTime = time.time() - startTime
        reqConfigDetails()
