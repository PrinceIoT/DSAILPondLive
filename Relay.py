import time

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO_PIN=3


GPIO.setup(GPIO_PIN, GPIO.OUT)
GPIO.output(GPIO_PIN, GPIO.LOW)

time.sleep(2)
GPIO.output(GPIO_PIN, GPIO.HIGH)

time.sleep(5)
GPIO.output(GPIO_PIN, GPIO.LOW)

time.sleep(2)
GPIO.output(GPIO_PIN, GPIO.HIGH)

time.sleep(5)
GPIO.output(GPIO_PIN, GPIO.LOW)

time.sleep(3)
GPIO.cleanup()