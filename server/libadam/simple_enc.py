import base64
class simple_encryption:
	#what is this, the days of charlemagne?
	#all the symmetric encryption modules for python are pish
	def __bitwise(self, password, string):
		encrstr = ''
		for x in xrange(0, len(string)):
			stringlet = ord(string[x])
			new_x = x
			passlet = ord(password[new_x])
			enclet = stringlet ^ passlet
			encrstr += chr(enclet)
		return encrstr
	def encrypt(self, password, string):
		return base64.b64encode(self.__bitwise(password, string))
	def decrypt(self, password, string):
		try:
			return self.__bitwise(password, base64.b64decode(string))
		except:
			return 'wrong'