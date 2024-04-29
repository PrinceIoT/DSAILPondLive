from gpiozero import DistanceSensor
from gpiozero import LED
import time
#Relay
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
time.sleep(2)

GPIO.setwarnings(False)

Ultrasonic=DistanceSensor(echo=26,trigger=6,max_distance=10)#threshold_distance=0.5);

Ultrasonic.threshold_distance=1.0

yellow_led=LED(23)
blue_led=LED(27)

while True:
    print(round(Ultrasonic.distance,3)*100)#Ultrasonic.distance)
    if Ultrasonic.distance < Ultrasonic.threshold_distance:
        #Ultrasonic.wait_for_in_range()
        #led=LED(23)
        print("Water level is high")
        GPIO.output(18,GPIO.LOW)
        yellow_led.off()
        blue_led.on()
      
    elif  Ultrasonic.distance > Ultrasonic.threshold_distance:
        print("Water Level is low")
        yellow_led.on()
        blue_led.off()
        GPIO.output(18, GPIO.HIGH)
        
    else:
        yellow_led.off()
        blue_led.on()
        print("In range")
    time.sleep(2)