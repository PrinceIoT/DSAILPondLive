import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os 
import glob
import time

#Relay and LED

from gpiozero import LED
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.output(18,GPIO.HIGH)
time.sleep(2)


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
    
file_path = "/home/pi/Documents/Localsensordata.txt"

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('pitest-395711-6e8443029bdf.json', scope)
client = gspread.authorize(credentials)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1IdUdQ7PsCzBy5q2TIc7WsBKfXKP24HXwtbi-Kh-9uxE/edit?usp=sharing').sheet1  # Replace with your sheet URL

while True:
    i=(read_temp())
    
    Turbidity_Val=(read_adc(0))*2
    Turb_Val=(-0.00159800708061275*(Turbidity_Val**2))+(-0.811711623495286*(Turbidity_Val))+3002.12125274895
    Turb_Val_1=round(Turb_Val,1)
    i_1=round((i),1)
    print("Turbidity Value is: ",Turb_Val_1,"NTU")   
    print("Water Temp: ",i_1,"*C")
    
    #Timestamps
    timestamp = time.localtime()
    f_time=time.strftime("%Y-%m-%d %H:%M:%S",timestamp)
    print(f_time)
    
    data_line=f"Timestamp: {f_time}, Water_Temp(*c):\t{i_1},  Turbidity(NTU): \t{Turb_Val_1}\n"        
    with open(file_path,"a") as file:
        file.write(data_line)

    # Append data to the Google Sheet
    sheet.append_row([f_time,i_1,Turb_Val_1])
    
    print("Sensor data saved successully")
    time.sleep(10)  # Delay between readings  