import threading
from functools import wraps

def thread(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		t = threading.Thread(target=func,args=args,kwargs=kwargs)
		t.start()
	return wrapper
