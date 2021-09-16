from filesystem.dir import Dir
from filesystem.file import File
from datetime import datetime

class Logger:

	def __init__(self, path, rid, verbose = False):
	
		self.path = Dir(path)
		self.verbose = verbose
		self.rid = rid
		self.hasError = False
		
		#Init dir
		
		if not self.path.exists():
			self.path.create()
		
	def log(self, section, status, message):
	
		log = '[' + datetime.today().strftime('%Y-%m-%d-%H:%M:%S') + '][' + section.upper() + '][' + status.upper() + '] - ' + message
	
		if self.verbose:
			print(log)
			
		f = open(self.path.getPath() + 'Log_' +  self.rid + '.log' , 'a')
		f.write(log + "\n")
		f.close()
		
		if status == 'error':
			self.hasError = True;
		
	def info(self, section, message):
		self.log(section,'info',message)
	
	def error(self, section, message):
		self.log(section,'error',message)
		
	def hasErrors(self):
		return self.hasError
		
	def purge(self, maxFilesCount):
	
		logs = sorted(self.path.list())

		for filename in logs[:(int(maxFilesCount)*-1)]:
			log = File(self.path.getPath()+filename)
			log.delete();