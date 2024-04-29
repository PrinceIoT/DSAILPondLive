from gpiozero import DistanceSensor
from gpiozero import LED
import time

Ultrasonic=DistanceSensor(echo=26,trigger=6,max_distance=10)#threshold_distance=0.5);
#Distance_cm=Ultrasonic_Distance.distance
#Ultrasonic.threshold_distance=1.0
#Ultrasonic.threshold_distance=8.0
led=LED(23)
#round(Ultrasonic.distance,3)*100