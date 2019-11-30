import MySQLdb
db = MySQLdb.connect("localhost", "jpipe", "jpipe", "myPrototype")
cursor = db.cursor()
sqlq="CREATE DATABASE JPipeAdaptor"
cursor.execute(sqlq)
sqlq="CREATE TABLE (ROLL_NO int(3),NAME varchar(20),SUBJECT varchar(20))"
cursor.execute(sqlq)
db.commit();
results = cursor.fetchone()
