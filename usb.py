import cv2
import numpy as np
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst


class USBCamera(object):

    def __init__(self, index):

	#Gst.init(None)

        #path = "v4l2src ! video/x-raw-yuv,width=720,height=480,framerate=20/1 ! appsink name=sink"+str(index)

	#self.pipe = Gst.parse_launch(path)

	#self.pipe.set_state(Gst.State.PLAYING)
	#self.appsink = self.pipe.get_by_name("sink"+str(index))
	#self.appsink.set_property("emit-signals", True)
	#self.appsink.set_property("max-buffers", 1)
	#self.appsink.set_property("drop", True)

	self.cap = cv2.VideoCapture(index)
	self.frame = np.zeros((720,480,3), np.uint8)



    def updateFrame(self):

        #sample = self.appsink.emit("pull-sample")

        #buf = sample.get_buffer()
        #caps = sample.get_caps()

        #self.frame = np.ndarray((caps.get_structure(0).get_value('height'),caps.get_structure(0).get_value('width'),3),buffer=buf.extract_dup(0, buf.get_size()),dtype=np.uint8)
	
	_,self.frame = self.cap.read()

