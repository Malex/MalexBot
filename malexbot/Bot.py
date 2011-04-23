import imp
from queue import Queue

from .Connection import Connection
from .Conf import Conf,ConfError
from .Parser import parse,ParserError
from .Thread import thread

class BotError(Exception):
	pass

class Bot():

	def __init__(self,conf,servers :dict=False,plugins_dir :str=""):
		self.conf = conf
		self.__connected = False
		if not servers:
			try:
				servers = conf['servers']
			except ConfError as e:
				raise BotError("You should set at least 1 server as default")
		self.__conns = []
		self.r_queue,self.s_queue = {},{}
		for i in servers:
			self.__conns.append(Connection(i,servers[i]))
			self.r_queue[i] = Queue()
			self.s_queue[i] = Queue()
		self.plugged = { 'on_msg' : [], 'on_load' : [], 'on_quit' : [] }
		for i in self.conf['plugins']:
			a = imp.load_module(i,*imp.find_module(i,plugins_dir))
			self.plugged['on_msg'].append(a.register.on_msg)
			self.plugged['on_load'].append(a.register.on_load)
			self.plugged['on_quit'].append(a.register.on_quit)

	def start(self):
		self.send()
		if not self.__connected:
			self.connect()
		self.recv()
		self.process()

	def connect(self):
		self.__connected = True
		for i in self.__conns:
			i.connect()
			for j in self.plugged['on_load']:
				j(self,conn)

	def close(self):
		for i in self.__conns:
			for j in self.plugged['on_quit']:
				j(self,conn)
			i.close()

	def recv(self):
		for i in self.__conns:
			self.recv_c(i)

	@thread
	def recv_c(self,conn):
		while True:
			r = conn.recv().decode(self.conf['server_encode'])
			for i in r.split('\r\n'):
				self.r_queue[conn.server].put_nowait(i)

	def process(self):
		for i in self.__conns:
			self.proc_c(i)

	@thread
	def proc_c(self,conn):
		while True:
			t = self.r_queue[conn.server].get()
			for i in self.plugged['on_msg']:
				i(self,conn,t)

	def send(self):
		for i in self.__conns:
			self.send_c(i)

	@thread
	def send_c(self,conn):
		while True:
			conn.send(self.s_queue[conn.server].get().encode(self.conf['server_encode']))
