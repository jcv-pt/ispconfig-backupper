import os

class File:

	def __init__(self, path):
	
		self.path = path
		
	def exists(self):
	
		return os.path.exists(self.path)
		
	def getPath(self):
		
		return self.path
		
	def getName(self):
	
		return os.path.basename(self.path)
		
	def getSize(self):
	
		return os.path.getsize(self.path)
  
	def create(self):
		
		open(self.path, 'a').close()
		
	def delete(self):
		
		os.remove(self.path)
		
	def empty(self):
	
		if self.exists(self.path):
			self.delete()
			
		self.create(self.path)
		