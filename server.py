
import socket
import sys
import thread


host = "10.15.59.6"

#port = 5805 #some legal port#
port = 5801 #5801

lock = thread.allocate_lock()


class Server(object):

	def __init__(self):

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.setblocking(1)
		host = socket.gethostname()
		self.s.bind(('',port))
		self.s.listen(5)


	def send(self,ti,ai,di):
		if self.c == None:
			return
		try:
			self.c.send("c"+str(ti)+"a"+str(ai)+"d"+str(di))
		except socket.error:
			pass


	def receive(self):
		if self.c == None:
			return
		try:
			r = self.c.recv(1024) #1024
			#print r
			return r
		except socket.error:
			pass


	def accept(self):
		try:
			self.c, ref = self.s.accept()
		except socket.error:
			self.c = None


	def close(self):
		if self.c == None:
			return
		self.c.close()


def startServer():
	thread.start_new_thread(run, ())


def run():
	#print "lime"
	s = Server()
	global t, a, d
	a = -1000
	d = 0
	t = "no target"

	global data
	data = "none"

	while 1:
		s.accept()
		data = s.receive()
		with lock:
			s.send(t,a,d)
			#try:
			#	data = s.receive()
			#except:
			#	return
			#s.send(t,a,d)
			#if(data == "s"):
				#s.send(cx)
		s.close()


def putData(target, angle, distance):
	#global t, a, d
	with lock:
            t = target
	    a = angle
            d = distance

def getData():

	return data

