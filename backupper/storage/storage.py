import boto3
from botocore.exceptions import ClientError
from progress import Progress

class Storage:

	def __init__(self, config, verbose=True):
		
		self.config = config
		self.verbose = verbose
		
		self.error = None
		self.client = boto3.Session().client(
			self.config.get('Storage','Type'), # service_name
			None, # region_name=None
			None, # api_version=None
			True, # use_ssl=True
			None, # verify=None
			self.config.get('Storage','Server') + ':' + self.config.get('Storage','Port'), # endpoint_url=None
			self.config.get('Storage','AccessKey'), # aws_access_key_id=None
			self.config.get('Storage','AccessKeySecret'), # aws_secret_access_key=None
			None, # aws_session_token=None
			None,# config=None
		)
		
	
	def getClient(self):
	
		return self.client
		
	def upload(self, file, fileFolder = None, fileName = None):
	
		filePath = "";
		
		# Set file folder
		if fileFolder is not None:
			filePath += fileFolder + '/'
			
		# Set file name
		if fileName is not None:
			filePath += fileName
		else:
			filePath += file.getName()

		# Upload the file
		try:
		
			#Set callback
			callback = None;
			
			if self.verbose is True:
				callback = Progress(file)
				
			# Upload 
			response = self.client.upload_file(file.getPath(), self.config.get('Storage','Path'), filePath, Callback=callback)
			
		except Exception as e:
			self.error = e
			return False
		return True

	def getError(self):
	
		return self.error
		
	def getMessage(self):
	
		return format(self.getError())