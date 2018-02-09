import cv2
import numpy as np
import calc
import LEDFinder
import cubeFinder


###DO MORE MATH###

class Stereo(object):

	#length is distance between cameras
	def __init__(self, finderR, finderL, length):
		
		self.finders = [finderR, finderL]

		self.errL = -1000
		self.errR = -1000

		self.errorAngle = -1000
		self.distanceToTarget = -1000

		self.length = length

		#MAX ANGLE TO POSSIBLE WITH CUBE IN FOV OF BOTH CAMERAS#
		self.maxAngle = 24.4 #just a guess right now
		


	def track(self):

		self.errL = self.errR = self.errorAngle = self.distanceToTarget = -1000
		
		for finder in self.finders:
			finder.find()

		if self.finders[0].found and self.finders[1].found: #both cameras see target
			self.errL = self.finders[1].err
			self.errR = self.finders[0].err
			dist = calc.getDistance(self.errR, self.errL, self.length) 
			self.errorAngle = calc.getCenterAngle(calc.getAngle(self.errR), calc.getAngle(self.errL), dist, self.length)
			self.distanceToTarget = calc.getDiagonalDistance(self.errorAngle, dist)

		elif not self.finders[0].found and self.finders[1].found: #only left cam sees target
			self.errorAngle = -self.maxAngle #spin to the left to find the target

		elif self.finders[1].found and not self.finders.found: #only the right cam sees target
			self.errorAngle = self.maxAngle #spin to the right to find the target
			
		#else neither camera sees it and all values set to -1000



class LEDStereo(object): #it's like a normal stereo, but with color and confidence

	def __init__(self, cameraR, cameraL, length):

		self.finderR = LEDFinder.LEDFinder(cameraR)
		self.finderL = LEDFinder(cameraL)

		self.stereo = Stereo(self.finderR, self.finderL, length)

		self.confidence = "n" #n,w,r,l

	def setRed(self):

		self.finderR.setRed()
		self.finderL.setRed()

	def setBlue(self):

		self.finderR.setBlue()
		self.finderL.setBlue()

	def track(self):

		self.stereo.track()
		#do some math with the confidence and other fun stuff#
