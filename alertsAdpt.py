import MySQLdb
import json

def data_process(data):
	db = MySQLdb.connect("localhost","root","root","jPipeAdptDb")
	j = json.loads(data)
	i = 0
	while i < len(j['get_alerts']):
		alert_executeon = j['get_alerts'][i]['Alert_ExecuteOn']
		if alert_executeon != 'Adapter':
			print("Aleret_ExecuteOn != Adapter, quitting")
			i = i + 1
			continue
		else:
			alert_id = int(j['get_alerts'][i]['AlertId'])
			alert_name = j['get_alerts'][i]['Alert_Name']
			alert_frequency = j['get_alerts'][i]['Alert_Frequency']
			alert_conditions = j['get_alerts'][i]['Alert_Conditions']

			for dict in alert_conditions:
				sqlq = "insert into alertsAdpt (AlertId, Alert_Name, Alert_Frequency, Alert_ExecuteOn, Field, condition1, condition2) values (" + str(alert_id) + ", \"" + alert_name + "\",\"" + alert_frequency + "\",\"" + alert_executeon + "\",\"" + dict['Field'] + "\",\"" + dict['condition1'] + "\",\"" + dict['condition2'] + "\")";

				print(sqlq);
				cursor = db.cursor()
				cursor.execute(sqlq)
				db.commit();
				results = cursor.fetchone()
				print(results)
		i = i + 1

data = input()

data_process(data)

print("Data added into db successfully !")

