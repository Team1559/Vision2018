import numpy as np
import cv2
import PID
import server
import usb
import cubeFinder
import stereo


cameraR = usb.USBCamera(0)
cameraL = usb.USBCamera(1)

cubeR = cubeFinder.CubeFinder(cameraR)
cubeL = cubeFinder.CubeFinder(cameraL)

stereo = stereo.Stereo(cubeR, cubeL, 8)

while 1:

	stereo.track()
	print "r"+str(stereo.finders[0].angle)
	print "l"+str(stereo.finders[1].angle)
	print "d"+str(stereo.distanceToTarget)

	cv2.imshow("r", stereo.finders[0].frame)
	cv2.imshow("l", stereo.finders[1].frame)
	cv2.waitKey(1)

	#print stereo.distanceToTarget()


