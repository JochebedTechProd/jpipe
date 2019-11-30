import paho.mqtt.client as mqttClient
import time
import AES_B64
cipher = AES_B64.AESCipher('0000000000000001')
def on_connect(client, userdata, flags, rc):
    global clientConnected, retryMqttConnection
    print "in on_connect"
    if rc == 0:
        print("Connected to broker")
        global Connected                #Use global variable
        clientConnected = True                #Signal connection 
        client.subscribe("jts/jpipe/v000001/adapter/1")
        toLoad = '{"key":"1"}'
        toPublish = cipher.encrypt(str(toLoad))
        print "toLoad=",toLoad,"="
        print "toPub=",toPublish,"="
        client.publish('jts/jpipe/v000001/adapter/adapter_config',toPublish)
    else:
        print("Connection failed")
        retryMqttConnection=True
def on_message(client, userdata, message):
    print ("Message received: "  + message.payload)
    strToDecode = message.payload
    appendText = cipher.decrypt(str(strToDecode))
    replText=appendText.replace('\\\"','\"')
    print(replText)
    file1 = open("configFile.txt","w+")
    file1.write(str(replText))
    file1.close()

global clientConnected, retryMqttConnection
client=mqttClient.Client()
client.on_connect=on_connect
client.on_message=on_message

client.username_pw_set(username="esp", password="ptlesp01")
#client.connect("localhost", 1883, 60)
clientConnected = False
client.connect("cld003.jts-prod.in", 1883, 60)

tempSentTime = time.time()
tempDataSendWaitTime = 3
tempDataSendWaitTime = 10
initialSetup = True

while(1):
    client.loop()
    elapsedTime = time.time() - tempSentTime
    if elapsedTime > tempDataSendWaitTime:
        print("Elapsed time: ", elapsedTime)
        tempSentTime = time.time()

