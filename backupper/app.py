import os
import argparse
import time

from datetime import datetime
from log.logger import Logger
from config.config import Config
from mysql.mysql import Mysql
from mysql.mysqldump import MysqlDump
from filesystem.dir import Dir
from filesystem.file import File
from server.server import Server
from storage.storage import Storage
from zip.zip import Zip
from utils.utils import Utils

class App:

	def run(self):
	
		# Initialize app args
		
		argParser = argparse.ArgumentParser(description='ISPConfig : Backupper - Archives and uploads ISPConfig instance client data to web storage')
		
		argParser.add_argument('--verbose', dest='verbose', type=int, default=1, help='Weather to display logging output')
		
		self.args = argParser.parse_args()

		# Initialize app var
	
		self.app = {
			'rid' : datetime.today().strftime('%Y-%m-%d_%H%M%S'),
			'stime' : time.time(),
			'sdate' : datetime.today().strftime('%Y-%m-%d'),
			'path' : os.path.abspath(os.getcwd()),
			'verbose' : bool(self.args.verbose)
		}
		
		# Initialize logger & config
		
		self.logger = Logger(self.app['path'] + '/data/logs/', self.app['rid'], self.app['verbose'])
		self.config = Config(self.app['path'] + '/data/config/default.ini')

		# Initialize libs - MYSQL
		
		mysql = Mysql(self.config)
		
		if mysql.connect() is False:
			self.logger.error('db',mysql.getMessage())
			exit(1)
			
		self.mysql = mysql.getConnection()
		
		# Initialize libs - MYSQLDUMP
		
		self.mysqldump = MysqlDump(self.config)
		
		# Initialize libs - STORAGE
		
		self.storage = Storage(self.config, self.app['verbose'])
		
		# Initialize working dir
		
		self.workingDir = Dir(self.config.get('Dirs','TempDir') + 'backupper/')
		
		if not self.workingDir.exists():
			self.workingDir.create()
		else:
			self.workingDir.empty()
			
		# Get server

		self.server = Server(self.mysql, 1)
		
		# Lookup clients, and process backups
		
		conditions = ""
		
		if self.config.get('Archive','SkipClientIds') is not None:
			conditions = "AND client.client_id NOT IN (" + self.config.get('Archive','SkipClientIds') + ")"
		
		self.mysql.execute("SELECT client.client_id, sys_group.groupid FROM client INNER JOIN sys_group ON sys_group.client_id = client.client_id WHERE 1 " + conditions + " ORDER by client.client_id ASC")

		lookup = self.mysql.fetchall()
		
		if len(lookup) > 0:
			self.logger.info('global', str(len(lookup)) + ' clients found, starting backup routines...')
		else:
			self.logger.info('global', 'No clients found!')

		for client in lookup:
		
			# Backup domains files
			
			self.processDomainFiles(client);
			
			# Backup databases
			
			self.processDatabases(client);
			
			# Backup mail accounts
			
			self.processMailAccounts(client);
		
		#Report
		
		self.logger.info('global', 'Process completed in ' + Utils.secondsToHours(time.time() - self.app['stime']))
		
		# Cleanup
		
		self.logger.purge(self.config.get('Logs','MaxFilesCount'))
		
		# Exit

		if self.logger.hasErrors() is True:
			exit(1)
		
		exit(0)

	def processDomainFiles(self, client):
	
		#Lookup client domains
		
		conditions = ""
		
		if self.config.get('Archive','SkipDomainIds') is not None:
			conditions += "AND web_domain.domain_id NOT IN (" + self.config.get('Archive','SkipDomainIds') + ") "
			
		if self.config.get('Archive','SkipDomainNames') is not None:
			domains = self.config.get('Archive','SkipDomainNames').split(',')
			conditions += "AND web_domain.domain NOT IN (" + Utils.arrayToQuotes(domains) + ") "

		self.mysql.execute("SELECT * FROM web_domain WHERE sys_groupid = " + str(client['groupid']) + " " + conditions)

		lookup = self.mysql.fetchall()
	
		for domain in lookup:
		
			# Compile client host dir
			
			domainDir = self.server.getWebsitePath(client['client_id'], domain['domain_id'])
			
			# Create archive
			
			archiveFile = File(self.workingDir.getPath() + self.app['rid'] + '_client_' + str(client['client_id']) + '_domain_' + str(domain['domain_id']) + '_'  + str(domain['domain']) + '.zip')

			archiveZip = Zip(archiveFile.getPath());
			
			status = archiveZip.compressDir(domainDir)
			
			if status :
				self.logger.info('domain', 'Archive for website #' + str(domain['domain_id']) + ' created')
			else:
				self.logger.err('domain', 'Failed creating archive for website #' + str(domain['domain_id']))
				continue
				
			# Upload to storage
			
			self.logger.info('database', 'Uploading file ' + archiveFile.getName() + ' to storage..')
			
			status = self.storage.upload(archiveFile, self.app['sdate']);
			
			if status is False:
				self.logger.error('domain',self.storage.getMessage())
			
			# Delete archive
			
			archiveFile.delete()
			
	
	def processDatabases(self, client):
	
		#Lookup client databases
	
		self.mysql.execute("SELECT database_name FROM web_database WHERE sys_groupid = " + str(client['groupid']) + " AND type = 'mysql' ORDER BY database_name")

		lookup = self.mysql.fetchall()
	
		for database in lookup:
	
			# Compile client database file
			
			databaseFile = File(self.workingDir.getPath() + self.app['rid'] + '_client_' + str(client['client_id']) + '_database_' + database['database_name'] + '.sql')
			
			# Create sql export
			
			status = self.mysqldump.run(database['database_name'], databaseFile.getPath())
			
			if status :
				self.logger.info('database', 'Database ' + database['database_name'] + ' exported')
			else:
				self.logger.error('database', 'Failed exporting database ' + database['database_name'])
				continue
				
			# Upload to storage
			
			self.logger.info('database', 'Uploading file ' + databaseFile.getName() + ' to storage...')
			
			status = self.storage.upload(databaseFile, self.app['sdate']);
			
			if status is False:
				self.logger.error('domain',self.storage.getMessage())
			
			# Delete export
			
			databaseFile.delete()
			
	def processMailAccounts(self, client):
	
		#Lookup client domains
		
		conditions = ""
			
		if self.config.get('Archive','SkipDomainNames') is not None:
			domains = self.config.get('Archive','SkipDomainNames').split(',')
			for domain in domains:
				conditions += "AND email NOT LIKE '%@" + domain + "' "
	
		self.mysql.execute("SELECT email, maildir FROM mail_user WHERE sys_groupid = " + str(client['groupid']) + " " + conditions + " ORDER BY email")

		lookup = self.mysql.fetchall()
	
		for email in lookup:
		
			# Create archive
			
			archiveFile = File(self.workingDir.getPath() + self.app['rid'] + '_client_' + str(client['client_id']) + '_email_' + email['email'] + '.zip')

			archiveZip = Zip(archiveFile.getPath());
			
			status = archiveZip.compressDir(email['maildir'])
			
			if status :
				self.logger.info('email', 'Archive for email ' + email['email'] + ' created')
			else:
				self.logger.error('email', 'Failed creating archive for email ' + email['email'])
				continue
				
			# Upload to storage
			
			self.logger.info('email', 'Uploading file ' + archiveFile.getName() + ' to storage...')
			
			status = self.storage.upload(archiveFile, self.app['sdate']);
			
			if status is False:
				self.logger.error('domain',self.storage.getMessage())
			
			# Delete archive
			
			archiveFile.delete()

