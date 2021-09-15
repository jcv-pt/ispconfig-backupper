import MySQLdb

class Mysql:

	def __init__(self, config):
	
		self.config = config;
		
		self.connected = None
		self.error = None
		
	def connect(self):
	
		if self.connected is None:
		
			try:
				self.conn = MySQLdb.connect(
					host=self.config.get('Mysql','Host'),
					user=self.config.get('Mysql','Username'),
					password=self.config.get('Mysql','Password'),
					database=self.config.get('Mysql','Database')
				)
			except Exception as e:
				self.error = e
				self.connected = False
			
			self.connected = True
			
		return self.connected

  	def getError(self):
	
		return self.error
		
	def getMessage(self):
	
		return format(self.getError())
		
	def getConnection(self):
		
		return self.conn.cursor(MySQLdb.cursors.DictCursor);
		
	def closeConnection(self):
		
		self.conn.close()