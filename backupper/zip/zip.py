import os
import zipfile

class Zip:

	def __init__(self, path):
	
		self.path = path
		
	def compressDir(self, dir, mode = 'w'):
	
		zip = zipfile.ZipFile(self.path, mode, zipfile.ZIP_DEFLATED)
	
		for root, dirs, files in os.walk(dir):
			for file in files:
				zip.write(os.path.join(root, file), 
						   os.path.relpath(os.path.join(root, file), 
										   os.path.join(dir, '..')))

		zip.close()
		
		return os.path.isfile(self.path)