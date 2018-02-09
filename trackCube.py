import numpy as np
import cv2
import PID
import server
import usb
import cubeFinder


p = PID.PID(0.0033,0,0,0,0,500,-500)
p.setPoint(0)

camera = usb.USBCamera(0)
cube = cubeFinder.CubeFinder(camera)

server.startServer()


while 1:

	cube.find()	
	
	if(cube.err != -1000):
		r = -(p.update(cube.err))
	else:
		r = 0
	print r
	#if cube.err > 0:
	#	r = 0.6
	#elif cube.err < 0:
	#	r = -.6

	#if abs(cube.err) <= 30:
	#	r = 0

	server.putData(0,0,r) 
	

