import ConfigParser

class Config:

	def __init__(self, file):
	
		self.storage = file
		self.handler = ConfigParser.ConfigParser()
		
		# Read

		self.handler.read(self.storage)

	def get(self ,section, key):
		
		return self.handler.get(section, key)
	