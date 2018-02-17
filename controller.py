import seven
import servo
import RPi.GPIO as GPIO
from socketIO_client_nexus import SocketIO, LoggingNamespace
socketIO = SocketIO("10.10.10.145", 3000, LoggingNamespace)

'''
-------Pin Setup
'''
GPIO.setmode(GPIO.BOARD)
ledErrorPin = 11
ledSuccessPin = 13
btnPin = 10

GPIO.setup(ledErrorPin, GPIO.OUT)
GPIO.setup(ledSuccessPin, GPIO.OUT)
GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def bersihbersih():
	GPIO.cleanup()

def denied():
	print("denied")
	GPIO.output(ledErrorPin, GPIO.HIGH)
	GPIO.output(ledSuccessPin, GPIO.LOW)

def granted():
	print("granted")
	servo.SetAngle(180)
	GPIO.output(ledErrorPin, GPIO.LOW)
	GPIO.output(ledSuccessPin, GPIO.HIGH)

def netral():
	print("netral")
	servo.SetAngle(0)
	GPIO.output(ledErrorPin, GPIO.LOW)
	GPIO.output(ledSuccessPin, GPIO.LOW)
	
def isBtnPressed():
	return not GPIO.input(btnPin)

'''
------- Event Handler
'''

def on_muka(nama):
	granted()
	print(isBtnPressed())
	if isBtnPressed():
		socketIO.emit("lock", "lock")
		netral()
	print(nama)

def on_denied(msg):
	denied()

def on_netral(msg):
	netral()
	
socketIO.on("muka", on_muka)
socketIO.on("denied", on_denied)
socketIO.on("netral", on_netral)
socketIO.wait()
