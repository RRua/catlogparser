import os,sys,re, json

LOG_LEVELS = { 
	# according to http://developer.android.com/tools/debugging/debugging-log.html
    "V": "verbose",
    "D": "debug",
    "I": "info",
    "W": "warn",
    "E": "error",
    "A": "assert",
    "F": "fatal",
    "S": "silent"
}

def getFormatRegex(log_format):
		# https://developer.android.com/studio/command-line/logcat#outputFormat
		return {
	        "threadtime": "^(\d{2}\-\d{2}) (\d\d:\d\d:\d\d\.\d+)\s*(\d+)\s*(\d+)\s([VDIWEAF])\s(.*)?:(.*)?$",
	    	#"brief": "([VDIWEAF])\/([^)]{0,23})?\\(\\s*(?<pid>\\d+)\\):\\s+(?<message>.*)$"
	    }[log_format]


class ErrorStats(object):
	def __init__(self):
		self.stats = {}
		for level in LOG_LEVELS.values():
			self.stats[level]=0

	def updateStat(self,obj):
		if "level" in obj:
			self.stats[obj["level"]]+=1

class LogCatParser(object):
	def __init__(self,log_format, filepath ):
		self.log_format = log_format
		self.format_regex = getFormatRegex(log_format)
		self.filepath = filepath
		self.parsedLines=[]
		self.stats=ErrorStats()

	def mergeLines(self,line_obj_to_merge):
		self.parsedLines[-1]["message"] += "\n"+line_obj_to_merge["message"]

	def canMergeLines(self,log_line_obj):
		if len(self.parsedLines)==0:
			return False
		last_parsed_line_id = self.getLogLineID( self.parsedLines[-1])
		return last_parsed_line_id == self.getLogLineID (log_line_obj)


	def getLogLineID(self,log_line_obj):
		date = "" if "date" not in log_line_obj else log_line_obj["date"]
		time = "" if "time" not in log_line_obj else log_line_obj["time"]
		pid  = "" if "pid" not in log_line_obj else log_line_obj["pid"]
		tid  = "" if "tid" not in log_line_obj else log_line_obj["tid"]
		level  = "" if "level" not in log_line_obj else log_line_obj["level"]
		return date+time+pid+tid+level


	def buildLogLine(self,log_line_groups):
		log_obj = {}
		if self.log_format == "threadtime":
			log_obj['date']   = log_line_groups[0]
			log_obj['time']   = log_line_groups[1]
			log_obj['pid']    = log_line_groups[2]
			log_obj['tid']    = log_line_groups[3]
			log_obj['level']  = LOG_LEVELS[ log_line_groups[4] ]
			log_obj['tag']    = log_line_groups[5]
			log_obj['message'] = log_line_groups[6]
		
		return log_obj


	def addParsedLine(self,parsed_obj):
		if self.canMergeLines(parsed_obj):
			self.mergeLines( parsed_obj )
		else:
			self.parsedLines.append( parsed_obj)
			self.stats.updateStat(parsed_obj)
	

	def parseFile(self):
		regex= getFormatRegex(self.log_format)
		f = open(self.filepath, "r")
		for line in f.readlines():
			x=re.search("%s" % regex, line)
			if x:
				parsed_obj = self.buildLogLine(x.groups())
				self.addParsedLine(parsed_obj)

		print( json.dumps( self.parsedLines,  indent=4) )

if __name__== "__main__":
	if len(sys.argv) > 1:
		filepath=sys.argv[1]
		log_format= sys.argv[2] if len (sys.argv)>2 else "threadtime"
		parser = LogCatParser(log_format,filepath)
		parser.parseFile()
		print(parser.stats.stats)

	else:
		print ("ERROR: at least one arg required <filename> (<logformat>)? )")


