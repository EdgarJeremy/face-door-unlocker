import cv2
import base64
from socketIO_client_nexus import SocketIO, LoggingNamespace
socketIO = SocketIO("10.10.10.145", 3000, LoggingNamespace)

camera = cv2.VideoCapture(0)

while True:
	ret, im = camera.read()
	small = cv2.resize(im, (0, 0), fx=0.30, fy=0.30)
	ret2, buf = cv2.imencode(".jpg", small)
	b64 = base64.b64encode(buf)
	socketIO.emit("stream", b64)
	cv2.imshow("Feed", im)
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break


cv2.destroyAllWindows()
camera.release()
