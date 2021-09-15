import os

from filesystem.file import File

class MysqlDump:

	def __init__(self, config):
	
		self.config = config
  
	def run(self, database, path):
	
		file = File(path)
		
		# Compile command 
		
		command = 'export MYSQL_PWD=' + self.config.get('Mysql','Password') + ' && mysqldump -h ' + self.config.get('Mysql','Host') + ' -u ' + self.config.get('Mysql','Username') + ' ' + database + ' > ' + file.getPath()
	
		os.system(command)

		return file.exists()