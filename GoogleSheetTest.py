import spidev
spi=spidev.SpiDev()
import time
import datetime
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
spi.open(0,0)
spi.max_speed_hz=1000000

#Light LED
from gpiozero import LED
yellow_led=LED(23)
blue_led=LED(27)

#Email
email="dsailraspberrypi23@gmail.com"
password="Raspberrypi@23"

spreadsheet = "Logging"

#Putting the exception call in python to attempt for logging in Gmail
try:
     ret = gspread.login(email,password)
except:
     print('Oops! Check Internet Connection or Login Credentials')
     sys.exit()

#open the spreadsheet by either of these two options
worksheet = ret.open(spreadsheet).Sheet1
#or with the spreadsheet key
#worksheet = ret.open_by_key("https://docs.google.com/spreadsheets/d/1f5ppZCWTMdyEWPLDbBbJGOYvyZQ2qsdXSj3KsVUE_7I/edit?usp=sharing")
#prefer First Option

def read_adc(channel):
    adc=spi.xfer2([1,(8+channel)<<4,0])
    data=((adc[1]&3)<<8)+adc[2]
    return data
def turb_to_volt(Turbidity_Val):
    voltage=((570-Turbidity_Val)/570)*2.5
    return voltage

while True:
    Turbidity_Val=read_adc(0)
    voltage=turb_to_volt(Turbidity_Val)
    values = [datetime.datetime.now(), voltage]
    worksheet.append_row(values)
    print(voltage,"V")
    if voltage<1.5:
        yellow_led.off()
        blue_led.on()
    else:
        yellow_led.on()
        blue_led.off()
    #print("Turbidity-Value is: ", Turbidity_Val ,"NTU")
    time.sleep(4)