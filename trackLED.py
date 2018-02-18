import numpy as np
import cv2
import PID
import server
import usb
import LEDFinder


#p = PID.PID(0.0033,0,0,0,0,500,-500)
#p.setPoint(0)

camera = usb.USBCamera(0)
#camera.setExposure(9)
led = LEDFinder.LEDFinder(camera)
led.setRed()
#led.setBlue()

#server.startServer()


while 1:

	led.find()	
	led.calculateConfidence()

	cv2.imshow("frame", led.frame)
	cv2.waitKey(1)

	#print led.confidence
	
	#print led.err	

	#if(led.err != -1000):
	#	r = -(p.update(cube.err))
	#else:
	#	r = 0
	#print r
	#if cube.err > 0:
	#	r = 0.6
	#elif cube.err < 0:
	#	r = -.6

	#if abs(cube.err) <= 30:
	#	r = 0

	#server.putData(0,0,r) 
	

