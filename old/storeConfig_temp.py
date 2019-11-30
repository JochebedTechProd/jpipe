#importing the requests library 
import requests
import json
  
  # api-endpoint 
URL = "https://cld003.jts-prod.in/JpipeAdapter/get_adapter_settings/"
username = "admin1"
password = "admin1"
AdapterId = "1"

  # defining a params dict for the parameters to be sent to the API 
PARAMS = '{"Username":"%s","Password":"%s","Adapter_id":"%s"}' %(username,password,AdapterId)
print(PARAMS)
  # sending get request and saving the response as response object 
r = requests.post(url = URL, data = PARAMS)
print()
print("resp=",r,"=")
jsonObj = eval(r.text)
print("jsonObj=",jsonObj,"=\n")
print(jsonObj['get_adapter_settings'][0]['settings'])
print(jsonObj)
file1 = open("configFile.txt","w+")
file1.write(str(jsonObj))
file1.close()
