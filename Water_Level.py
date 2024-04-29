from gpiozero import DistanceSensor
from gpiozero import LED
import time

Ultrasonic=DistanceSensor(echo=26,trigger=6,max_distance=10)#threshold_distance=0.5);
#Distance_cm=Ultrasonic_Distance.distance
#Ultrasonic.threshold_distance=1.0
#Ultrasonic.threshold_distance=8.0
led=LED(23)
#round(Ultrasonic.distance,3)*100
while True:
    di=round(Ultrasonic.distance,3)*100
    print("distance:",di,"cm")#Ultrasonic.distance)
    if Ultrasonic.distance > 50:#Ultrasonic.threshold_distance:
        #Ultrasonic.wait_for_in_range()
        #led=LED(23)
        led.on()
        print("Water level is high")
    elif  Ultrasonic.distance > 100:#Ultrasonic.threshold_distance1:
        print("Water Level is low")
        led.on()
    else:
    #Ultrasonic.wait_for_out_of_range()
        led.off()
        print("In range")
    time.sleep(5)
    