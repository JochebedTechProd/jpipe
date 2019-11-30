import json

# some JSON:
x =  '{ "name":"John", "age":30, "city":"New York"}'

# parse x:
y=json.loads(x)

# the result is a Python dictionary:
print(y["age"])


jsonText='{"error_code":"200","Response":"Successfully got 1 details", "get_adapter_settings":[{"setting_id":"3","settings":{"input_folder":"/basefolder/in","out_folder":"/basefolder/out"}}]}'
parsedJson=json.loads(jsonText)
print(parsedJson["get_adapter_settings"][0])
