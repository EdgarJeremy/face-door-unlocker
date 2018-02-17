import cv2
import numpy as np
import base64
from threading import Thread
from socketIO_client_nexus import SocketIO, LoggingNamespace
import face_recognition
import os
import glob

socketIO = SocketIO("localhost",3000,LoggingNamespace)

'''
------------- Prep Recognition
'''
folder = "../faces/"
list_faces = []
array_faces_encoding = []
list_file = os.listdir(folder)
for face_file in list_file:
	image = face_recognition.load_image_file(folder + face_file)
	print(face_file)
	print(len(face_recognition.face_encodings(image)))
	encoding = face_recognition.face_encodings(image)[0]
	list_faces.append({face_file: encoding})
	array_faces_encoding.append(encoding)
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
tabuka = False
cropPadding = 15
	
def read(b64_string):
	nparr = np.fromstring(b64_string.decode("base64"), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img

def on_lock(lock):
	global tabuka
	print(lock)
	tabuka = False

def on_stream(strm):

	global tabuka
	global face_names
	global cropPadding

	small_frame = read(strm)
	masuk = None

	if not tabuka:
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
					name = name.split("_")[0]

			face_names.append(name)

		print(len(face_names))

		if len(face_names) > 0:
			if face_names[0] == "Tidak Dikenali":
				socketIO.emit("denied", face_names)
				masuk = None
			else:
				socketIO.emit("muka",face_names[0])
				masuk = face_names[0]
				tabuka = True
				rec = folder + str(face_names[0]) + ("_" + str(len(glob.glob1(folder, face_names[0] + "_*")) + 1)) + ".jpg"
				print(rec)
				print(face_locations[0])
				(top, right, bottom, left) = face_locations[0]
				height, width, channel = small_frame.shape
				print(height)
				print(width)
				top = 0 if (top - cropPadding) < 0 else (top - cropPadding)
				bottom = height if (bottom + cropPadding) > height else (bottom + cropPadding)
				left = 0 if (left - cropPadding) < 0 else (left - cropPadding)
				right = width if (right + cropPadding) > width else (right + cropPadding)
				print((top, right, bottom, left))
				cv2.imwrite(rec, small_frame[top:bottom, left:right])
		else:
			socketIO.emit("netral", face_names)
			masuk = None

	else:
		socketIO.emit("muka",face_names[0])


	cv2.imshow("Feed", small_frame)
	cv2.waitKey(1)
	

socketIO.on("stream", on_stream)
socketIO.on("lock", on_lock)
socketIO.wait()
