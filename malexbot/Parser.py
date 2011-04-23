import re

__reg = re.compile(r":?(((?P<nick>[\w\[\]\^`]+)!(?P<user>[\w\[\]\^`]+)@(?P<host>.+?))\s+|(?P<server>.*?)|)(?P<type>[A-Z0-9]+)\s(?P<chan>#[\w\[\]\^`]+|)\s?(?P<sender>[\w\[\]\^`]+|)\s*:(?P<mex>.+)",re.DOTALL)

class ParserError(ValueError):
	pass

def parse(s :str) -> dict:
	try:
		global __reg
		return __reg.match(s).groupdict()
	except BaseException as e:
		raise ParserError("Unable to match string {}".format(s)) from e
