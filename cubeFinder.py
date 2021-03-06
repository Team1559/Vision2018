import cv2
import numpy as np
import calc


class CubeFinder(object):

    def __init__(self, Camera):
	
	self.camera = Camera
	
	self.cx = -1
	self.cy = -1
	self.err = -1000

	self.hsvl = np.array((15,0,50))
	self.hsvh = np.array((30,255,255))

	self.width = 640
	self.height = 480

	self.found = False

	self.minarea = 20000

	self.angle = -1000

	self.frame = np.zeros((1920,1080,3), np.uint8)


    def find(self):
	
	self.camera.updateFrame()
	self.frame = self.camera.frame

	self.cx = self.cy = -1

	#convert to hsv
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv, self.hsvl, self.hsvh)

	threshcp = thresh.copy()

	#blur me 
	thresh = cv2.blur(thresh, (3,3))

	#erode and dilate
	thresh = cv2.erode(thresh, (3,3))
	thresh = cv2.dilate(thresh, (3,3))

	threshcp = thresh.copy()
	

        #find some contours
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        #grab the one biggest areas
        contours = sorted(contours, key=cv2.contourArea, reverse = True)[:5]

        #find centroids of contours
        best_cnt = None
        for cnt in contours:

		#print cv2.contourArea(cnt)
		#print cv2.isContourConvex(cnt)

        	if cv2.contourArea(cnt) < self.minarea:
        		continue

		#approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
	        #print len(approx)
		
		best_cnt = cnt
		break
		

	

	if best_cnt == None:
	    self.found = False
	    self.cx = self.cy = -1
	    self.err = self.angle = -1000
	else:
	    self.found = True

            M1 = cv2.moments(best_cnt)
            self.cx,self.cy = int(M1['m10']/M1['m00']), int(M1['m01']/M1['m00'])

	    self.err = self.cx-(self.width/2)

	    self.angle = calc.getAngle(self.err)

	    cv2.circle(self.frame,(self.cx,self.cy),5,255,-1)

	#cv2.imshow("frame", self.frame)
	#cv2.imshow("hsv", threshcp)
	#cv2.waitKey(1)




		


