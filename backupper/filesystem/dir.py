import os, shutil

class Dir:

	def __init__(self, path):
	
		self.path = path
		
	def exists(self):
	
		return os.path.isdir(self.path)
		
	def getPath(self):
		
		return self.path
  
	def create(self):
		
		os.mkdir(self.path)
		
	def list(self):
	
		return os.listdir(self.path)
		
	def empty(self):
	
		for filename in os.listdir(self.path):
			file_path = os.path.join(self.path, filename)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				print('Dir : Failed to delete %s. Reason: %s' % (file_path, e))
		