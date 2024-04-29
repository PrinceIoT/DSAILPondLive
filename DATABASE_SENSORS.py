import mysql.connector
from datetime import datetime

sensor_name = "POND"

timestamp = datetime.now()

#TURBIDITY
import spidev
spi=spidev.SpiDev()
import time
spi.open(0,0)
spi.max_speed_hz=1000000
def read_adc(channel):
    adc=spi.xfer2([1,(8+channel)<<4,0])
    data=((adc[1]&3)<<8)+adc[2]
    return data
    
#Water Temperature
import glob
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


#Ultrasonic, Relay and LED
from gpiozero import DistanceSensor
from gpiozero import LED
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)
time.sleep(2)

Ultrasonic=DistanceSensor(echo=26,trigger=6,max_distance=10)
Ultrasonic.threshold_distance=1.0

yellow_led=LED(23)
blue_led=LED(27)
#Ultrasonic distance module
def Ultra_distance():
    
    if  distance_cm< (Ultrasonic.threshold_distance)*100:
         print("Water level is high")
         GPIO.output(18,GPIO.HIGH)
         yellow_led.off()
         blue_led.on()
         
    elif distance_cm > (Ultrasonic.threshold_distance)*100:
        print("Water Level is low")
        yellow_led.on()
        blue_led.off()
        GPIO.output(18, GPIO.LOW)
    else:
    
        yellow_led.off()
        print("In range")

#Database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456789",
  database="TEST21"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE sensor_data (id INT AUTO_INCREMENT PRIMARY KEY, sensor_name VARCHAR(255), Water_Temp_C FLOAT,Turbidity_Val_NTU FLOAT,distance_cm FLOAT,timestamp TIMESTAMP)")

while True:
    #Water Temp
	Water_Temp_C=(read_temp())
	Turbidity_Val_NTU=read_adc(0)
	
	#Ultrasonic
	distance_cm=(round(Ultrasonic.distance,3))*100
	x=Ultra_distance()
	
	#PRINTS
	print("Distance: ",distance_cm,"cm")
	print("Turbidity-Value is: ", Turbidity_Val_NTU ,"NTU")
	print ("Water_Temp is: ",Water_Temp_C, 'Degree Celsius')
	print("Batch done")
	
	time.sleep(5)
	sql = "INSERT INTO sensor_data (sensor_name, Water_Temp_C,Turbidity_Val_NTU,distance_cm, timestamp) VALUES (%s, %s, %s,%s,%s)"
	val = (sensor_name, Water_Temp_C,Turbidity_Val_NTU,distance_cm, timestamp)
	mycursor.execute(sql, val)
	mydb.commit()
	