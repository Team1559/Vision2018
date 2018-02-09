from __future__ import division
import cv2
import numpy as np
import calc



class LEDFinder(object):

	def __init__(self, camera): #find me PLZ
		
		self.camera = camera
		self.cx = -1
		self.cy = -1
		self.err = -1000
		self.angle = -1000
		#self.x = self.y = -1

		self.rightx = -1
		self.leftx = -1

		self.points = []

		self.width = 640
		self.height = 480

		self.found = False
		self.minarea = 20 #small guy???????????

		self.color = "no color"

		self.frame = np.zeros((1920,1080,3), np.uint8)

		self.confidence = "n" #n is no LEDs, w is LEDs centered, l is LEDs to the left, r is LEDS to the right

		self.red = [
		       np.array((5,100,180)),
		       np.array((255,255,255))
		      ]

#np.array((10,200,185)),np.array((45,255,255))

		self.blue = [
		       np.array((0,0,0)),
		       np.array((255,255,255))
		      ]

		#params = cv2.SimpleBlobDetector_Params()
		#params.filterByArea = True
		#params.minArea = 0

		#params.filterByCircularity = True
		#params.minCircularity = 0.01

		#self.detector = cv2.SimpleBlobDetector(params)

		#self.i = 0
		#self.px = -1
		#self.py = -1
		#self.c = 0


	def find(self):

		self.camera.updateFrame()
		self.frame = self.camera.frame

		self.cx = self.cy = -1
		self.err = self.angle = -1000
		self.points = []
		
		thresh = np.zeros((self.height,self.width,3), np.uint8)

		#convert to hsv and threshold the image
		hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
		if self.color is 'red':
        		thresh = cv2.inRange(hsv, self.red[0], self.red[1])
			threshcp = thresh.copy()	
		elif self.color is 'blue':
			thresh = cv2.inRange(hsv, self.blue[0], self.blue[1])
			threshcp = thresh.copy()
		else:
			print "invalid target color"
        		return

		#blur me 
		thresh = cv2.blur(thresh, (4,4))

		#erode and dilate
		thresh = cv2.erode(thresh, (1,1))
		thresh = cv2.dilate(thresh, (1,1))

		#threshcp = thresh.copy()

		#find some contours
        	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        	#grab the 10 biggest areas
        	contours = sorted(contours, key=cv2.contourArea, reverse = True)[:30]

        	#find centroids of contours
        	cnts = []
        	for cnt in contours:
	
			#print cv2.contourArea(cnt)
			#print cv2.isContourConvex(cnt)

        		if cv2.contourArea(cnt) < self.minarea:
        			continue

			approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
			#print len(approx)

			#circley
			if 8 < len(cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)) < 25:
				cnts.append(cnt)
		
		
		if len(cnts) == 0:
	    		self.found = False
	        	self.cx = self.cy = -1
	        	self.err = -1000
		else:
		        self.found = True

	        	for cnt in cnts:
			     #print cv2.isContourConvex(cnt)
            	    	     M1 = cv2.moments(cnt)
		             x = int(M1['m10']/M1['m00'])
                             y = int(M1['m01']/M1['m00'])
			     self.points.append([x,y,cnt])
			     cv2.circle(self.frame,(int(x),int(y)),5,255,-1)
			     #self.cx += x
			     #self.cy += y

			self.average()
	
	                #self.cx = (self.cx / len(cnts)) + 1
	                #self.cy = (self.cy / len(cnts)) + 1
			#print self.cx

			#self.x += self.cx
			#self.y += self.cy
			#self.i += 1

			#if(self.i == 5):
			#	self.x = self.x / 5
			#	self.y = self.y / 5
			#	self.i = 0
				#print self.x
				#cv2.line(threshcp,(int(self.x),0),(int(self.x),480),255,3,8,0)
				#cv2.line(threshcp,(0,int(self.y)),(640,int(self.y)),255,3,8,0)
	
			

	                #self.err = self.cx-(self.width/2)

	        	#cv2.circle(frame,(int(self.cx),int(self.cy)),5,255,-1)

	        cv2.imshow("frame", self.frame)
	        cv2.imshow("cnt", thresh)
		cv2.imshow("hsv", threshcp)
	        cv2.waitKey(1)


	def average(self):
		
		#x = y = 0
		rightmost = -1
		leftmost = self.width + 1
		for pt in self.points:
			if pt[0] < leftmost:
				leftmost = pt[0]
			if pt[0] > rightmost:
				rightmost = pt[0]
			#x += self.points[0][0]

		#x = x/len(self.points)
		self.cx = (leftmost+rightmost)/2
		self.rightx = rightmost
		self.leftx = leftmost

		self.err = self.cx-(self.width/2)
		self.angle = calc.getAngle(self.err)
		#print leftmost
		#print len(self.points)

		cv2.line(self.frame,(int(self.cx),0),(int(self.cx),480),255,3,8,0)


	def calculateConfidence(self): #kinda bad but ok for now, use stereo angle probably later but we'll see

		if not self.found:		
			self.confidence = "n"

		elif self.rightx > self.width/2 and self.leftx < self.width/2:
			self.confidence = "w"

		elif self.leftx > self.width/2:
			self.confidence = "r"

		elif self.rightx < self.width/2:
			self.confidence = "l" 

	def setRed(self):
		self.color = "red"

	def setBlue(self):
		self.color = "blue"


