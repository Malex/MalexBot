import imp

class ConfError(Exception):
	pass

class Conf:
	def __init__(self,filename :str):
		self.conf = self.parse(filename)
		try:
			self.update_conf(self.query("conf_chain"))
		except ConfError:
			pass

	def parse(self,file :str) -> dict:
		""" Open the configuration file and save its values
		in a dictionary. It is run by the constructor, you
		don't need to call this method """
		return vars(imp.load_source("conf",file))

	def query(self,key :str):
		""" Returs a configuration value """
		try:
			return self.conf[key]
		except KeyError as e:
			raise ConfError("Incomplete configuration: {} key not found".format(key)) from e

	def update_conf(self,path :str):
		""" Add Conf values from another conf file. Note that values may be overridden """
		self.conf.update(self.parse(path))

	def __getitem__(self,key :str):
		return self.query(key)
