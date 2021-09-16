class Utils:

	@staticmethod
	def arrayToQuotes(items, quote = "'"):
		i = 1
		compiled = ""
		for item in items:
			compiled += quote + item + quote
			if i < len(items):
				compiled += ","
			i += 1 
		return compiled
	
	@staticmethod
	def secondsToHours(seconds):
		seconds = seconds % (24 * 3600)
		hour = seconds // 3600
		seconds %= 3600
		minutes = seconds // 60
		seconds %= 60
		  
		return "%d:%02d:%02d" % (hour, minutes, seconds)