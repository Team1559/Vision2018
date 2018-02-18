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
		self.upy = -1
		self.downy = -1

		self.points = []

		self.width = 640
		self.height = 480

		self.found = False
		self.minarea = 20 #small guy???????????

		self.color = "no color"

		self.frame = np.zeros((self.width,self.height,3), np.uint8)

		self.confidence = "n" #n is no LEDs, w is LEDs centered, l is LEDs to the left, r is LEDS to the right

		self.red = [
		       np.array((5,100,160)),
		       np.array((200,255,255))
		      ]

#np.array((10,200,185)),np.array((45,255,255))

		self.blue = [
		       np.array((100,100,180)),
		       np.array((160,255,255))
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
		
		self.i = 0
		self.averages = []
		self.averagex = -1
		self.averagey = -1
		#self.oldFrame = np.zeros((self.width,self.height,3), np.uint8)


	def find(self):

		self.camera.updateFrame()

		self.frame = self.camera.frame

		self.cx = self.cy = -1
		self.err = self.angle = -1000
		self.points = []
		
		thresh = np.zeros((self.width,self.height,3), np.uint8)

		self.frame = cv2.blur(self.frame, (3,3,))
		self.frame = cv2.erode(self.frame, (1,1))
		self.frame = cv2.dilate(self.frame, (1,1))

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


		#if self.i is 0: #take first frame and save it
		#	self.oldFrame = thresh
		#	cv2.imshow("1st frame", self.oldFrame)
		#	self.i += 1
			#return
		#elif self.i is 2: #combine the images
		#	newFrame = thresh
		#	self.thresh = cv2.addWeighted(self.oldFrame, 1.0, newFrame, 1.0, 0.0)
		#	cv2.imshow("2nd frame", newFrame)
		#	cv2.imshow("blended", thresh)
		#	self.i = 0
		#else:
		#	self.i += 1

		#blur me 
		thresh = cv2.blur(thresh, (3,3))

		#erode and dilate
		thresh = cv2.erode(thresh, (1,1))
		thresh = cv2.dilate(thresh, (1,1))

		threshcp = thresh.copy()

		#find some contours
        	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        	#grab the 10 biggest areas
        	contours = sorted(contours, key=cv2.contourArea, reverse = True)[:100]

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
			     cv2.circle(self.frame,(int(x),int(y)),5,100,-1)
			     #self.cx += x
			     #self.cy += y

			self.average()
			self.calculateConfidence()
	
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

	        #cv2.imshow("frame", self.frame)
	        cv2.imshow("cnt", thresh)
		cv2.imshow("hsv", threshcp)
	        #cv2.waitKey(1)


	def average(self):
		
		#x = y = 0
		rightmost = -1
		leftmost = self.width + 1
		downmost = -1
		upmost = self.height + 1
		for pt in self.points:
			if pt[0] < leftmost:
				leftmost = pt[0]
			if pt[0] > rightmost:
				rightmost = pt[0]
			if pt[1] < upmost:
				upmost = pt[1]
			if pt[1] > downmost:
				downmost = pt[1]
			#x += self.points[0][0]

		#x = x/len(self.points)
		self.cx = (leftmost+rightmost)/2
		self.cy = (upmost+downmost)/2
		
		self.upy = upmost
		self.downy = downmost
		self.rightx = rightmost
		self.leftx = leftmost

		self.err = self.cx-(self.width/2)
		self.angle = calc.getAngle(self.err)
		#print leftmost
		#print len(self.points)

		
		if len(self.averages) >= 5:
			self.averages.remove(self.averages[0])
		self.averages.append([self.cx, self.cy])
		
		self.averagex = 0
		self.averagey = 0
		for num in self.averages:
			self.averagex += num[0]
			self.averagey += num[1]
		self.averagex = self.averagex / len(self.averages)
		self.averagey = self.averagey / len(self.averages)
		print self.averagex

		cv2.line(self.frame,(int(self.averagex),0),(int(self.averagex),480),(0,255,0),3,8,0)
		cv2.line(self.frame,(0,int(self.averagey)),(640,int(self.averagey)),(0,255,0),3,8,0)


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


