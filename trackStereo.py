import stereo
import cv2
import numpy as np
import usb


cameraR = usb.USBCamera(0)
cameraL = usb.USBCamera(1)

cubes = stereo.Stereo(cameraR, cameraL, 8)
lights = stereo.LEDStereo(cameraR, cameraL, 8)


lights.setRed() #change this based on data from server


while 1:

	lights.track()
	cv2.imshow("right", lights.finderR.frame)
	cv2.imshow("left", lights.finderL.frame)
	cv2.waitKey(1)
