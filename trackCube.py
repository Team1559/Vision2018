import numpy as np
import cv2
import PID
import server
import usb
import cubeFinder


p = PID.PID(0.0037,0,0,0,0,500,-500)
p.setPoint(0)

camera = usb.USBCamera(0)
cube = cubeFinder.cubeFinder(camera)

server.startServer()


while 1:

	cube.find()	
	
	if(cube.err != -1000):
		r = -(p.update(cube.err))
	else:
		r = 0
	print r

	server.putData(0,0,r)



