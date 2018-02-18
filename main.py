import cv2
import numpy as np
import stereo
import server
import LEDFinder
import cubeFinder
import calc
import usb
import PID


camera = usb.USBCamera(0)
#cameraR and cameraL


#cubes = stereo.Stereo(cameraR, cameraL, 8)
#lights = stereo.LEDStereo(cameraR, cameraL, 8)
cube = cubeFinder.CubeFinder(camera)



target = "none"


server.startServer()


while 1:

	target = server.getData()
	print target

	if target is "c":
		cube.find()
		server.putData("c",cube.angle,0)
	#if target is "r":
	#	if lights.getColor() is not "red":
	#		lights.setRed()
	#	lights.track()
	#	server.putData("r",lights.angle,lights.distance)
	#if target is "b":
	#	if lights.getColor() is not "blue":
	#		lights.setBlue()
	#	lights.track()
	#	server.putData("b",lights.angle,lights.distance)
