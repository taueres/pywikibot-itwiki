#!/usr/bin/python
import os, sys, re
from settings import MAX_LOG_SIZE

def isArchivedLog ( fileName ) :
	return re.search( '^[0-9]{3}\.log$', fileName )

def getLogFileName ( number ) :
	strNum = str( number )
	leadingZeros = 3 - len ( strNum )
	return "0" * leadingZeros + strNum + ".log"

def getNextLogFile ( previousLogFile ) :
	index = int( previousLogFile[:-4] )
	newIndex = index + 1
	return getLogFileName ( newIndex )

notArchivedFile = os.environ['LOG_FILE_LINGUE']
if not os.path.isfile( notArchivedFile ) :
	# No file to rotate, quitting
	sys.exit( 0 )
size = os.path.getsize( notArchivedFile )
#size = 13000

if size < MAX_LOG_SIZE :
	# Rotation not needed, quitting
	sys.exit( 0 )

logDir = os.path.dirname( notArchivedFile )
files = os.listdir( logDir )
files = filter( isArchivedLog, files )
files = sorted( files )
latestArchive = files[-1]
newLogFile = getNextLogFile( latestArchive )

os.rename( notArchivedFile, logDir + "/" + newLogFile )
