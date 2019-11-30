import AES_B64
import paho.mqtt.client as mqttClient
import time
import uuid
import json
import random
# joins elements of getnode() after each 2 digits.

print ("The MAC address in formatted way is : ")
print (''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                 for ele in range(0, 8 * 6, 8)][::-1]))
macAd=''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                 for ele in range(0, 8 * 6, 8)][::-1])
CLIENT_ID_REG=1
devReg=False
devRegPubTopic = "jts/jpipe/v000001/adaptorRegPub"
devRegSubTopic = "jts/jpipe/v000001/"+macAd
print(devRegSubTopic)
subTopic = "jts/jpipe/v000001/adaptor/"+str(CLIENT_ID_REG)
devPubTopic = "jts/"
cipher = AES_B64.AESCipher('1234567812345668')
cipher = AES_B64.AESCipher('0000000000000001')
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")
def on_message(client, userdata, message):
    print ("Message received: "  + message.payload)
    strToDecode = message.payload
    appendText = cipher.decrypt(str(strToDecode))
    replText=appendText.replace('\\\"','\"')
    print(replText)
    return
    file1 = open("configFile.txt","w+")
    file1.write(str(replText))
    file1.close()
    print(userdata)
    if(message.topic == devRegSubTopic):
        print("Recieved response for reg")
        devReg = True
    strToDecode = message.payload
    appendText = cipher.decrypt(str(strToDecode))
    print(appendText)
    fileConfig = open("configFileMqtt.txt","r+")
    configText = fileConfig.readline()
    print fileConfig.readline()
    print("config text="+configText)
    repConfigText = configText.replace("'",'"')
    #jsonObj = configText.json()
    jsonObj = json.loads(repConfigText)
    print("pasrse successful");
    print(jsonObj['get_adapter_settings'][0])
    print((jsonObj['get_adapter_settings'][0]['settings']['input_folder']))
    fileConfig.close()
    filenm = jsonObj['get_adapter_settings'][0]['settings']['input_folder'].encode('ascii','ignore')
    filenm = filenm.replace("<baseFolder>",".")
    filenm = filenm+"/file"+str(time.time())+".in"
    print "repl filename=",filenm,"="
    file1 = open(filenm,"w+")#write mode 
    file1.write(appendText) 
    file1.close()
    #with open(filenm, 'a+') as f:
        #print "Message received: " + appendText
        # f.write("Message received: " + appendText + "\n")
def execFunc(user,password,on_connect,on_message,broker_address,inPort,inSubTopic):
    global mqttClient
    #client = mqttClient.Client("Python")  # create new instance
    #client.username_pw_set(user, password=password)  # set username and password
    #client.on_connect = on_connect  # attach function to callback
    #client.on_message = on_message  # attach function to callback
    #client.connect(broker_address, port=int(inPort))  # connect to broker
    #client.subscribe(inSubTopic)
    #client.loop_start()


Connected = False  # global variable for the state of the connection

broker_address = "cld003.jts-prod.in"  # Broker address
var_port = 1883  # Broker port
var_user = "esp"  # Connection username
var_password = "ptlesp01"  # Connection password

client = mqttClient.Client("Python")  # create new instance
client.username_pw_set(var_user, var_password)  # set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
client.connect(broker_address, var_port,60)  # connect to broker
print "sub topic=",subTopic
client.subscribe(subTopic)
#client.subscribe(parmTopic)
client.subscribe(devRegSubTopic)
client.loop_start()  # start the loop

startTime = time.time()
inpParmLastCheckTime = time.time()
inpParmLastCheckInt = 10

while (1):  
    client.loop()
    continue
    if (time.time()-inpParmLastCheckTime>inpParmLastCheckTime):
        inpParmLastCheckTime=time.time()+inpParmLastCheckInt

    jsonObj = json.load(open('configFile.json', 'r'))
    print("mqttUSer : " ,jsonObj["Settings"]["mqttUser"])
    print("mqttPort : " ,jsonObj["Settings"]["mqttPort"])
    print("mqttPassword : ",jsonObj["Settings"]["mqttPassword"])
    print("mqttServer : " ,jsonObj["Settings"]["mqttServer"])
    new_mqttUser = jsonObj["Settings"]["mqttUser"]
    new_mqttPort = jsonObj["Settings"]["mqttPort"]
    new_mqttPassword = jsonObj["Settings"]["mqttPassword"]
    new_mqttServer = jsonObj["Settings"]["mqttServer"]
    #execFunc(mqttUser,mqttPassword,on_connect,on_message,mqttServer,mqttPort,subTopic)
    #client = mqttClient.Client("Python")  # create new instance
    #client.username_pw_set(mqttUser, password=mqttPassword)  # set username and password
    #client.on_connect = on_connect  # attach function to callback
    #client.on_message = on_message  # attach function to callback
    #client.connect(broker_address, port=port)  # connect to broker
    #client.subscribe(subTopic)
    #client.subscribe(devRegSubTopic)
    #client.loop_start()  # start the loop
'''
try:
    while (True):
        f = open("demofile.txt", "r")
        for i in f:
            print(i)
            tempStr = i
            tempStr.replace("\n","")
            print(cipher.encrypt(i))
            #pubStr = f.readline()
            client.publish("jts/jpipe/v000001/adapter/device_operation",cipher.encrypt(i))
        f.close()
        #time.sleep(5)
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
'''


