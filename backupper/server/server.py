import ConfigParser
import StringIO

class Server:

	def __init__(self, mysql, id):
	
		self.mysql = mysql
		self.id = id
		
		self.config = ConfigParser.ConfigParser()
		
		# Get server data from db
		
		self.mysql.execute("SELECT * from server WHERE server_id = " + str(self.id))

		lookup = self.mysql.fetchone()
		
		# Read config

		buf = StringIO.StringIO(lookup['config'])
		self.config.readfp(buf)

		
	def getConfig(self ,section, key):
	
		return self.config.get(section, key)
		
	def getWebsitePath(self ,client, website):
	
		template = self.config.get('web','website_path')
		
		# Replace client and website ids
	
		template = template.replace("[client_id]", str(client))
		template = template.replace("[website_id]", str(website))
		
		return template