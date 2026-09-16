import RPi.GPIO as GPIO
import time

BUZZER = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)

GPIO.output(BUZZER, GPIO.HIGH)

time.sleep(2)

GPIO.output(BUZZER, GPIO.LOW)

GPIO.cleanup()
