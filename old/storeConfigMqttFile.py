import paho.mqtt.client as mqttClient
import time
############################################################################################################
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
        print("Connection failed")
############################################################################################################
def on_message(client, userdata, message):
    print ("Message received: "  + message.payload)
    #client.publish("mos/bikes1",message.payload)
    file1 = open("configFileMqtt.txt","w+")
    strToDecode = message.payload
    inMessage=""
    inMessage = cipher.decrypt(str(strToDecode))
    file1.write(str(inMessage))
    file1.close()
############################################################################################################

Connected = False   #global variable for the state of the connection 
broker_address= "cld003.jts-prod.in"  #Broker address
port = 1883                         #Broker port
user = "esp"                    #Connection username
password = "ptlesp01"            #Connection password
client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
client.loop_start()        #start the loop 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
client.subscribe("jts/jpipe/v000001/Adaptor/1")

try:
    username="admin1"
    password="admin1"
    AdapterId="1"
    PARAMS = '{"Username":"%s","Password":"%s","Adapter_id":"%s"}' %(username,password,AdapterId)
    print(PARAMS)

    print(cipher.encrypt(PARAMS))
    #pubStr = f.readline()
    client.publish("jts/jpipe/v000001/adapter/device_operation",cipher.encrypt(PARAMS))

except:
      print("An exception occurred")
try:
    while True:
        time.sleep(1)
        print("Running ....")
except:
      print("An exception occurred")
