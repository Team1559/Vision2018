
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


	def send(self,xi,yi,ri):
		#print "dad"
		if self.c == None:
			return
		try:
			self.c.send("x"+str(xi)+"y"+str(yi)+"r"+str(ri))
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
	print "lime"
	s = Server()
	global x,y,r
	x = y = r = -1000
	while 1:
		s.accept()
		#r = s.receive()
		with lock:
			s.send(x,y,r)
			#s.receive()
			#if(r == "s"):
				#s.send(cx)
		s.close()


def putData(xi, yi, ri):
	global x, y, r
	with lock:
            x = xi
	    y = yi
            r = ri

