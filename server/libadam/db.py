from warnings import filterwarnings
import MySQLdb
filterwarnings('ignore', category = MySQLdb.Warning)
# MYSQL class made as a technical test for dedsert by Adam Marc Jeanes.
# usage:
# import dedsert
# db = dedsertDB('ip', '3306', 'user', 'password' 'database')
# db.create_user('Adam Marc Jeanes', 22, 'Server Developer')
# db.list_users()
class adamDB():
	def __init__(self, ip, port, user, password, database):
		self.__server = ip
		self.__port = port #this might be superfulous
		self.__database = database
		self.__db_user = user #yeah, yeah, ethical hacker and all that
		self.__db_pass = password
	def __startDBop(self):
		self.__DB = MySQLdb.connect(self.__server, self.__db_user, self.__db_pass, self.__database)
		self.datastore = self.__DB.cursor()
	def __stopDBop(self):
		del self.datastore
	def sanitize(self, string):
		try:
			self.__startDBop()
			sanitized_string = self.__DB.escape_string(string)
			self.__startDBop()
			return sanitized_string
		except:
			return string
	def execute(self, cmd, insert=False):
		self.__startDBop()
		if(self.datastore):
			self.datastore.execute(cmd)
			output = self.datastore.fetchall()
			if(insert == True):
				self.__DB.commit()
			self.__stopDBop()
			return output
		else:
			print 'DB error'
			self.__stopDBop()