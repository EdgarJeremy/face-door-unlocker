import RPi.GPIO as GPIO
import time

sevenPin = [22, 18, 19, 21, 23, 24, 26]
pinDict = {
	"A": 0,
	"B": 1,
	"C": 2,
	"D": 3,
	"E": 4,
	"F": 5,
	"G": 6
}

GPIO.setmode(GPIO.BOARD)

for pin in sevenPin:
	GPIO.setup(pin, GPIO.OUT)
	

def hitung(angka):
	angka = 0 if angka > 9 else angka
	if angka == 1:
		mati()
		GPIO.output(ambilPin("B"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
	elif angka == 2:
		mati()
		GPIO.output(ambilPin("A"), GPIO.HIGH)
		GPIO.output(ambilPin("B"), GPIO.HIGH)
		GPIO.output(ambilPin("G"), GPIO.HIGH)
		GPIO.output(ambilPin("E"), GPIO.HIGH)
		GPIO.output(ambilPin("D"), GPIO.HIGH)
	elif angka == 3:
		mati()
		GPIO.output(ambilPin("A"), GPIO.HIGH)
		GPIO.output(ambilPin("B"), GPIO.HIGH)
		GPIO.output(ambilPin("G"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
		GPIO.output(ambilPin("D"), GPIO.HIGH)
	elif angka == 4:
		mati()
		GPIO.output(ambilPin("F"), GPIO.HIGH)
		GPIO.output(ambilPin("G"), GPIO.HIGH)
		GPIO.output(ambilPin("B"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
	elif angka == 5:
		mati()
		GPIO.output(ambilPin("A"), GPIO.HIGH)
		GPIO.output(ambilPin("F"), GPIO.HIGH)
		GPIO.output(ambilPin("G"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
		GPIO.output(ambilPin("D"), GPIO.HIGH)
	elif angka == 6:
		mati()
		GPIO.output(ambilPin("A"), GPIO.HIGH)
		GPIO.output(ambilPin("F"), GPIO.HIGH)
		GPIO.output(ambilPin("G"), GPIO.HIGH)
		GPIO.output(ambilPin("E"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
		GPIO.output(ambilPin("D"), GPIO.HIGH)
	elif angka == 7:
		mati()
		GPIO.output(ambilPin("F"), GPIO.HIGH)
		GPIO.output(ambilPin("A"), GPIO.HIGH)
		GPIO.output(ambilPin("B"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
	elif angka == 8:
		mati()
		for pin in sevenPin:
			GPIO.output(pin, GPIO.HIGH)
	elif angka == 9:
		mati()
		GPIO.output(ambilPin("A"), GPIO.HIGH)
		GPIO.output(ambilPin("F"), GPIO.HIGH)
		GPIO.output(ambilPin("B"), GPIO.HIGH)
		GPIO.output(ambilPin("G"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
		GPIO.output(ambilPin("D"), GPIO.HIGH)
	elif angka == 0:
		mati()
		GPIO.output(ambilPin("A"), GPIO.HIGH)
		GPIO.output(ambilPin("F"), GPIO.HIGH)
		GPIO.output(ambilPin("E"), GPIO.HIGH)
		GPIO.output(ambilPin("D"), GPIO.HIGH)
		GPIO.output(ambilPin("C"), GPIO.HIGH)
		GPIO.output(ambilPin("B"), GPIO.HIGH)


def mati():
	for pin in sevenPin:
		GPIO.output(pin, GPIO.LOW)
		

def ambilPin(huruf):
	return sevenPin[pinDict[huruf]]
