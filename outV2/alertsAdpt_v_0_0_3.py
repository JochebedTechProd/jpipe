import time
from datetime import datetime
import os
import json
import MySQLdb

def commLayer():
	data = raw_input()
	return data

def jsondata_process(data):

	alert_conditions = data['get_alerts'][0]['Alert_Conditions']

	if len(alert_conditions) != 2:
		print "Error Code 301. Quitting"
		return 0

	if alert_conditions[0]['PinsType'] != "occurTime" or alert_conditions[1]['operation'] != "value":
		print "Error code 302. Quitting"
		return 0

	os.system('echo \"' + str(data) + '\" >> alertAdpt.json')

	alert_frequency = data['get_alerts'][0]['Alert_Frequency']

db = MySQLdb.connect("localhost", "jtsac", "ptljtsac", "jPipeAdptDb")

cursor = db.cursor()
data = commLayer()
data = json.loads(data)
jsondata_process(data)
elapsed_time=time.strftime("%H:%M:%S")
alert_frequency = data['get_alerts'][0]['Alert_Frequency']

while(1):
	t1 = time.strftime("%H:%M:%S")
	tdelta = datetime.strptime(t1, "%H:%M:%S") - datetime.strptime(elapsed_time, "%H:%M:%S") 
	# print tdelta
	if ( tdelta >= (datetime.strptime(alert_frequency, "%H:%M:%S") - datetime.strptime("00:00:00", "%H:%M:%S"))):
		data = commLayer()
		data = json.loads(data)
		if jsondata_process(data) == 0:
			elapsed_time=time.strftime("%H:%M:%S")
			continue
		alert_frequency = data['get_alerts'][0]['Alert_Frequency']
		operator1 = data['get_alerts'][0]['Alert_Conditions'][0]['operator1']
		value1 = int(data['get_alerts'][0]['Alert_Conditions'][0]['value1'])	
		operator2 = data['get_alerts'][0]['Alert_Conditions'][0]['operator2']
		value2 = int(data['get_alerts'][0]['Alert_Conditions'][0]['value2']	)	

		if 'operator2_1' in data['get_alerts'][0]['Alert_Conditions'][1]:
			operator2_1 = data['get_alerts'][0]['Alert_Conditions'][1]['operator1']
			value2_1 = int(data['get_alerts'][0]['Alert_Conditions'][0]['value1'])
		else:
			operator2_1 = None
			value2_1 = -1

		if 'operator2_2' in data['get_alerts'][0]['Alert_Conditions'][1]:
			operator2_2 = data['get_alerts'][0]['Alert_Conditions'][1]['operator2']
			value2_2 = int(data['get_alerts'][0]['Alert_Conditions'][1]['value2'])
		else:
			operator2_2 = None
			value2_2 = -1

		curr_time = time.time()

		t1 = curr_time - (value1*60)
		t2 = curr_time - (value2*60)

		t1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t1))
		t2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t2))

		sqlq = "select data from inData WHERE inserrtDt BETWEEN \"" + t2 + "\" AND \"" +  t1 + "\""

		print sqlq

		cursor.execute(sqlq)

		db.commit();

		results = cursor.fetchall()

		print results
		a=[]
		for list_result in results:
			# val = list_result['data']['data']

			# eval_str = "val" + condition2_1 + value2_1 + ' and ' + "val" + condition2_2 + value2_2

			# if eval(eval_str):
			# 	print list_result
			h=json.loads(list_result)
			a.append(h['data'])
			sum1=sum(a)

			count1= len(a)
	   		
	   		avg= sum1/count1
	   		print avg
	   		print count1
		elapsed_time=time.strftime("%H:%M:%S")
