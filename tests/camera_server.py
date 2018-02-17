import cv2
import numpy as np
import base64
from threading import Thread
from socketIO_client_nexus import SocketIO, LoggingNamespace

socketIO = SocketIO("localhost",3000,LoggingNamespace)

	
def read(b64_string):
	nparr = np.fromstring(b64_string.decode("base64"), np.uint8)
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	return img
	

def on_stream(strm):
	print(read(strm))
	cv2.imshow("Feed", read(strm))
	cv2.waitKey(1)
	# imstream = read(strm)
	

socketIO.on("stream", on_stream)
socketIO.wait()
