import datetime
import face_recognition
import cv2
import base64
import os
import RPi.GPIO as GPIO
from time import sleep
from pygame import mixer
import seven
import servo

'''
-------Functions
'''

def bersihbersih():
	GPIO.cleanup()
	video_capture.release()
	cv2.destroyAllWindows()


def denied():
	GPIO.output(ledErrorPin, GPIO.HIGH)
	GPIO.output(ledSuccessPin, GPIO.LOW)

def granted():
	alertSukses.play()
	GPIO.output(ledErrorPin, GPIO.LOW)
	GPIO.output(ledSuccessPin, GPIO.HIGH)

def neutral():
	GPIO.output(ledErrorPin, GPIO.LOW)
	GPIO.output(ledSuccessPin, GPIO.LOW)
	
def isBtnPressed():
	return not GPIO.input(btnPin)


mixer.init()
alertPintuTerbuka = mixer.Sound("./sfx/beep.wav")
alertSukses = mixer.Sound("./sfx/success.wav")

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

video_capture = cv2.VideoCapture(0)

list_faces = []
array_faces_encoding = []
list_file = os.listdir("./faces")
for face_file in list_file:
	image = face_recognition.load_image_file("./faces/" + face_file)
	encoding = face_recognition.face_encodings(image)[0]
	list_faces.append({face_file: encoding})
	array_faces_encoding.append(encoding)

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

detect_mode = True
waktu_pintu_terbuka = datetime.datetime.now()
servoToggle = 180

try:
	while True:
		ret, frame = video_capture.read()
		sekarang = datetime.datetime.now()
		waktu = sekarang.strftime("%Y-%m-%d %H:%M:%S")
		
		if isBtnPressed():
			detect_mode = True
		
		if detect_mode:
			ret, frame = video_capture.read()
			small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

			if process_this_frame:
				face_locations = face_recognition.face_locations(small_frame)
				face_encodings = face_recognition.face_encodings(small_frame, face_locations)

				face_names = []
				for face_encoding in face_encodings:
					match = face_recognition.compare_faces(array_faces_encoding, face_encoding)
					name = "Tidak Dikenali"

					for index,item in enumerate(match):
						if item == True:
							face_dict = list_faces[index]
							name = list(face_dict.keys())[0].replace(".jpg","").replace(".jpeg","")
							name = name.replace(".jpeg","").title()

					face_names.append(name)

			process_this_frame = not process_this_frame


			for (top, right, bottom, left), name in zip(face_locations, face_names):
				top *= 4
				right *= 4
				bottom = (bottom * 4) + 40
				left *= 4

				cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 0), 2)
				cv2.rectangle(frame, (left - 4, top - 4), (right + 4, bottom + 5), (255, 255, 255), 2)

				cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 0), cv2.FILLED)
				font = cv2.FONT_HERSHEY_SIMPLEX
				cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

			if(len(face_names) > 0):
				if(face_names[0] == "Tidak Dikenali"):
					denied()
				else:
					granted()
					waktu_pintu_terbuka = sekarang
					detect_mode = False
			else:
				neutral()
			
		
		if not detect_mode:
			if servoToggle == 180:
				servo.SetAngle(0)
				servoToggle = 0
			lama = (sekarang - waktu_pintu_terbuka).seconds
			seven.hitung(lama)
			if lama >= 10:
				alertPintuTerbuka.play()
		else:
			if servoToggle == 0:
				servo.SetAngle(180)
				servoToggle = 180
			seven.mati()
		
		cv2.putText(frame,waktu,(10,30),cv2.FONT_HERSHEY_DUPLEX,1.0,(255,255,255),1)
		cv2.imshow('Webcam Output', frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	
	bersihbersih()
	
	
except KeyboardInterrupt:
	bersihbersih()
