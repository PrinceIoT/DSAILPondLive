import mysql.connector
from datetime import datetime

sensor_name = "sensor1"
#sensor_value = 25.6
timestamp = datetime.now()

import glob
import time
import os
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="TEST21"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE sensor_data (id INT AUTO_INCREMENT PRIMARY KEY, sensor_name VARCHAR(255), sensor_value FLOAT, timestamp TIMESTAMP)")

while True:
	sensor_value=(read_temp())
	print (sensor_value, 'Degree Celsius')	
	time.sleep(10)
	sql = "INSERT INTO sensor_data (sensor_name, sensor_value, timestamp) VALUES (%s, %s, %s)"
	val = (sensor_name, sensor_value, timestamp)
	mycursor.execute(sql, val)
	mydb.commit()
	#mydb.close()