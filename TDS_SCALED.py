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
#def turb_to_volt(Turbidity_Val):
   # voltage=((570-Turbidity_Val)/570)*2.5
   # return voltage

#Turb=adc_to_turb()

while True:
    Turbidity_Val=(read_adc(0))*2
    #voltage=turb_to_volt(Turbidity_Val)
    
    #Turbidity_NTU=((Turbidity_Val*2)-1024)/-0.25575
    #Turb_Val=(-300.7518797*(Turbidity_Val**2))+(436.0902256*(Turbidity_Val))+3685.714286588
    Turb_Val=(-0.00159800708061275*(Turbidity_Val**2))+(-0.811711623495286*(Turbidity_Val))+3002.12125274895 

    print(Turbidity_Val,Turb_Val)
    if Turbidity_Val  <1.5:
        yellow_led.off() 
        blue_led.on()
    else:
        yellow_led.on()
        blue_led.off()
    #print("Turbidity-Value is: ", Turbidity_Val ,"NTU")
    time.sleep(4)