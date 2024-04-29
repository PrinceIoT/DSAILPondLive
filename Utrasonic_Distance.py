import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#set up pins
TRIG_PIN=6
ECHO_PIN=26

while True:
    GPIO.setup(TRIG_PIN,GPIO.OUT)
    GPIO.setup(ECHO_PIN,GPIO.IN)

    #set the trig pin
    GPIO.output(TRIG_PIN,False)
    time.sleep(0.1)
    GPIO.output(TRIG_PIN,True)
    
    time.sleep(0.00001)
    
    #Set the echo pin
    StartTime=time.time()
    StopTime=time.time()
    
    #save the start time
    while GPIO.input(ECHO_PIN)==0:
        StartTime=time.time()
    #Save stop time
    while GPIO.input(ECHO_PIN)==1:
        StopTime=time.time()
        
    #Calculate time taken
    Duration=StopTime-StartTime
    
    # Calculation Distance
    distance=(Duration*343200)/2
    
    distance=round(distance,2)
    
    print("Distance is: ", distance, "cm")
    time.sleep(5)
    
    
    
        
    
    
    
    
    
    
    
    
    
    