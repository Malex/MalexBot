from functools import wraps

class PluginError(Exception):
	pass


class Register():

	def __init__(self):
		self.on_load = []
		self.on_quit = []
		self.on_msg = []

	def __call__(self,func,when):
		if not when in ["on_load","on_quit","on_msg"]:
			raise PluginError("Not valid option: {}".format(when))
		@wraps(func)
		def wrapper(self,conn,*args,**kwargs):
			self.s_queue[conn.server].put_nowait(func(*args,**kwargs))
		self.__dict__[when].append(wrapper)

register = Register()
