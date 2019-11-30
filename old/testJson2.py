import json
fileConfig = open("configFile.txt","r+")
configText = fileConfig.readline()
print("config text="+configText)
#jsonObj = configText.json()
jsonObj = json.loads(configText)
print("pasrse successful");
print(jsonObj['get_adapter_settings'][0])
print(eval(jsonObj['get_adapter_settings'][0]['settings']['input_folder']))
print(eval(jsonObj['get_adapter_settings']))
