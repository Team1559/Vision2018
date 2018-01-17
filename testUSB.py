import usb
import cv2


camera = usb.USBCamera(0)

while 1:
	camera.updateFrame()
	cv2.imshow("frame", camera.frame)
	cv2.waitKey(1)
