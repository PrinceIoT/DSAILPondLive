import spidev
spi=spidev.SpiDev()
import time
spi.open(0,0)
spi.max_speed_hz=1000000

#Light LED
from gpiozero import LED
yellow_led=LED(23)
blue_led=LED(27)

def read_adc(channel):
    adc=spi.xfer2([1,(8+channel)<<4,0])
    data=((adc[1]&3)<<8)+adc[2]
    return data
def turb_to_volt(Turbidity_Val):
    voltage=((570-Turbidity_Val)/570)*2.5
    return voltage
Cal_data=[(0,1130),(4000,0)]
def cal_fun(data):
    x_1,y_1=data[0]
    x_2,y_2=data[1]
    slope=(y_2-y_1)/(x_2-x_1)
    intercept=y_1-(slope*x_1)
    return slope, intercept
slope,intercept=cal_fun(Cal_data)
def adc_to_turb(adc_val):
    return (adc_val-intercept)/slope
#Turb=adc_to_turb()

while True:
    Turbidity_Val=(read_adc(0))*2
    voltage=turb_to_volt(Turbidity_Val)
    
    #Turbidity_NTU=((Turbidity_Val*2)-1024)/-0.25575
    Turb=round(adc_to_turb(Turbidity_Val),2)
    
    print(Turbidity_Val,Turb,voltage)
    if Turbidity_Val  <1.5:
        yellow_led.off()
        blue_led.on()
    else:
        yellow_led.on()
        blue_led.off()
    #print("Turbidity-Value is: ", Turbidity_Val ,"NTU")
    time.sleep(4)