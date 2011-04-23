import socket

class Connection():

	def __init__(self,server :str,port :int=6667):
		self.__conn = socket.socket()
		self.server = server
		self.port = port

	def connect(self):
		self.__conn.connect((self.server,self.port))

	def recv(self,max_data_size :int=4096) -> bytes:
		return self.__conn.recv(max_data_size)

	def send(self,data :bytes):
		if data:
			self.__conn.send(data)

	def close(self):
		self.__conn.close()

	def __delete__(self):
		self.close()
		del self.server
		del self.port
		del self.__conn
