import cv2
import numpy as np


class targetFinder(object):

    def __init__(self, Camera):
	
	self.camera = Camera
	
	self.cx = -1
	self.cy = -1
	self.err = -1000

	self.hsvl = np.array((30,0,0))
	self.hsvh = np.array((75,255,255))

	self.width = 720
	self.height = 480

	self.found = False

	self.minarea = 100


    def find(self):
	
	self.camera.updateFrame()
	frame = self.camera.frame

	self.found = False
	self.cx = self.cy = -1

	#convert to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, self.hsvl, self.hsvh)
        threshcp = thresh.copy()

	#blur me 
	thresh = cv2.blur(thresh, (5,5))

	#erode and dilate
	thresh = cv2.erode(thresh, (3,3))
	thresh = cv2.dilate(thresh, (3,3))

        #find some contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #grab the two biggest areas
        contours = sorted(contours, key=cv2.contourArea, reverse = True)[:2]

        #find centroids of contours
        self.i = 0
        for cnt in contours:

		#print cv2.contourArea(cnt)

		self.found = True
        	if cv2.contourArea(cnt) < self.minarea:
        		self.cx = self.cy = -1
        		self.found = False
        		break;


        	M1 = cv2.moments(cnt)
        	x1,y1 = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])


        	self.cx += x1
        	self.cy += y1



	if(self.found):

	    self.cx = (self.cx+1)/2
  	    self.cy = (self.cy+1)/2

	    self.err = self.cx-(self.width/2)

	    cv2.circle(frame,(self.cx,self.cy),5,255,-1)

	    cv2.imshow("frame", frame)
	    cv2.imshow("hsv", threshcp)
	    cv2.waitKey(1)

	else:
	    self.err = -1000


		


