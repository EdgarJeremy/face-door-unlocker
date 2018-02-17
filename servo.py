import RPi.GPIO as GPIO
from time import sleep

servoPin = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)

pwm = GPIO.PWM(servoPin, 50)
pwm.start(0)

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(servoPin, True)
	pwm.ChangeDutyCycle(duty)
