from __future__ import division
import math


#Camera Calculations for IMX219 Camera Sensor
hfov = 62.2 #horizontal
vfov = 48.8 #vertical
maxwidth = 3240
maxheight = 2464


def getAngle(error): #error angle when camera flipped on side

	err = error
	angle = 0.0

	angle = math.atan(err / 1115) #2715.9 for imx, 1115 for usb
	angle = math.degrees(angle)
	angle = round(angle,2)

	return angle



#lengtht is distance between cameras
def getDistance(errR, errL, length): #plane to plane distance from cameras to target

    if errL - errR == 0:
	return -1000
    return (length*maxwidth)/(2*math.tan(math.radians(vfov/2))*(abs(errL-errR))) #use vertical fov bc flipped on side


def getCenterAngle(angR, angL, dist, length): #error angle from midpoint of cameras [right angle, left angle, plane to plane distance, length between cameras]


    if abs(angL) > abs(angR): #on the right
        theta = round(dist/((length/2)-(dist/math.tan(math.radians(90-angL)))),3)
    elif abs(angR) > abs(angL): #on the left
        theta = -1*round(dist/((length/2)-(dist/math.tan(math.radians(90-angR)))),3)
    elif angR == angL:
    	theta = 0 #dead on
    else:
        theta = -1000

    return theta


def getDiagonalDistance(angE, dist): #pt to pt distance from center of cameras to target [center error angle, plane to plane distance]

	return dist/math.cos((math.radians(angE)))


