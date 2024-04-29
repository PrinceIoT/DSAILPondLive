import os
import glob
import time

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
#TDS MODULES
import spidev
spi=spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

#DS18B20 MODULES 
 
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
    
#TDS MODULES
def read_adc(channel):
    adc=spi.xfer2([1,(8+channel)<<4,0])
    data=((adc[1]&3)<<8)+adc[2]
    return data

def turb_to_volt(Turbidity_Val):
    voltage=((570-Turbidity_Val)/570)*2.5
    return voltage
#Ultrasonic distance module
def Ultra_distance():
    #if Ultrasonic.distance < Ultrasonic.threshold_distance:
    if distance_cm < (Ultrasonic.threshold_distance)*100:
         print("Water level is high")
         GPIO.output(18,GPIO.HIGH)
         yellow_led.off()
         blue_led.on()
         
    #elif  Ultrasonic.distance > Ultrasonic.threshold_distance:
    elif distance_cm > (Ultrasonic.threshold_distance)*100:
        print("Water Level is low")
        yellow_led.on()
        blue_led.off()
        GPIO.output(18, GPIO.LOW)
    else:
    
        yellow_led.off()
        print("In range")
    time.sleep(2)
    
#Loop
while True:
    #Temperature Module
    #di=round(Ultrasonic.distance,3)*100
	i=(read_temp())
	distance_cm=round(Ultrasonic.distance,3)*100
	
	#TDS MODULES
	Turbidity_Val=read_adc(0)
	voltage=turb_to_volt(Turbidity_Val)
	print("Turbidity Value is: ",voltage,"V")
	x=Ultra_distance()
	
	#Outputs
	#print("Turbidity-Value: ", Turbidity_Val ,"NTU")
	print ("Water Temp is: ",i, 'Degree Celsius')
	
	print("Distance: ",distance_cm,"cm")
	
	