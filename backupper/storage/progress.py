import sys
import threading

class Progress(object):

	def __init__(self, file):
	
		self.filename = file.getPath()
		self.totalSize = float(file.getSize())
		self.totalUploaded = 0
		self.lock = threading.Lock()

	def __call__(self, bytes_amount):
		
		with self.lock:
			
			self.totalUploaded += bytes_amount
			
			percentage = (self.totalUploaded / self.totalSize) * 100
			uploaded = self.getHumanSize(self.totalUploaded)
			size = self.getHumanSize(self.totalSize)
			
			sys.stdout.write("\rUploading file '%s' %s / %s  (%.2f%%) " % (self.filename, uploaded, size, percentage))
			sys.stdout.flush()
			
			if self.totalUploaded >= self.totalSize:
				sys.stdout.write("\n")
				
	def getHumanSize(self, num, suffix='B'):
		
		for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
			if abs(num) < 1024.0:
				return "%3.1f%s%s" % (num, unit, suffix)
			num /= 1024.0
		
		return "%.1f%s%s" % (num, 'Yi', suffix)