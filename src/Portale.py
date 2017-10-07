#coding: UTF-8

import simplejson as json
import urllib.request, urllib.error, urllib.parse, os, sys, time
import pywikibot, re
from pprint import pprint
from settings import LIMIT_TEMPLATE_CHECK, savePage

# Constants
SUMMARY = "[[WP:Bot|Bot]]: Fix portali in ordine alfabetico"
REGEX = r'\{\{[ \n]*([Tt]emplate: *)?([Pp]ortale|[Pp]rogetto|[Pp]ortali)[ \n]*\|[^\{\}]*\}\}'
REGEX_COMPILED = re.compile( REGEX )
TEMPLATE = "Template:Portale"
LIMIT_PAGES = 100
URL = ( "https://it.wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=" + TEMPLATE +
	"&einamespace=0&eilimit=" + str( LIMIT_PAGES ) + "&format=json" )
URL_CONTINUE = "eicontinue"
ERROR_LOG_PAGE = "Utente:TauerBot/Portale"

# Variables
wikiSite = pywikibot.getSite()
errorList = []

## Start counters
examinedPages = 0
numRequests = 0
error = 0
noSortingNeeded = 0
alreadySorted = 0
## End counters

# Functions
def getJsonFromURL( url ):
	response = urllib.request.urlopen( url )
	text = response.read()
	jsonData = json.loads( text )
	return jsonData

def getListPage( dictionaryList ):
	output = []
	for entry in dictionaryList:
		output.append( entry['title'] )
	return output

def getPageText( pageTitle ):
	wikiPage = pywikibot.Page( wikiSite, pageTitle )
	if not wikiPage:
		return False
	if wikiPage.isRedirectPage():
		return False
	return wikiPage.get()

def putPageText( pageTitle, text ):
	wikiPage = pywikibot.Page( wikiSite, pageTitle )
	savePage(wikiPage, text, SUMMARY)

def getPortalArguments( portalTemplate ):
	output = portalTemplate.split( '|' )
	output.pop( 0 ) # Take away the template itself
	lastIndex = len( output ) - 1

	if lastIndex < 0 :
		# Empty list?
		# This shouldn't happen (see regex we used)
		return False

	if '}}' not in output[lastIndex] :
		# Template is not closed
		# This shouldn't happen (see regex we used)
		return False
		
	# Remove }} closing template from the last element
	output[lastIndex] = output[lastIndex].replace( '}}', '' )

	# Strip leading and trailing spaces
	# Removing empty arguments
	delIndex = []
	for (i, elem) in enumerate(output):
		output[i] = elem.strip()
		if not output[i] :
			delIndex.append( i )
	# Set delIndex in descending order: pop will overwrite the indexes
	delIndex.reverse()
	for ind in delIndex :
		output.pop( ind )
	return output

def generatePortal( arguments ):
	output = "{{Portale"
	for argument in arguments :
		output += '|' + argument
	output += '}}'
	return output

# Force edit when empty arguments are present or template Progetto is used
def editForced( portalTemplate ):
	rawArgs = portalTemplate.split( '|' )
	for arg in rawArgs :
		if not arg :
			return True
	if 'progetto' in rawArgs[0].lower() :
		return True
	if 'portali' in rawArgs[0].lower() :
		return True
	if 'template' in rawArgs[0].lower() :
		return True
	if '\n' in rawArgs[0] :
		return True
	return False

def saveErrorLog( errorPages, wikiPageTitle ):
	if len( errorPages ) == 0 :
		return
	wikiPage = pywikibot.Page( wikiSite, wikiPageTitle )
	if not wikiPage :
		raise Exception( 'Error while getting wikiPageTitle' )
	if wikiPage.exists() :
		output = wikiPage.get()
	else :
		output = "In questa pagina vengono elencate le voci che hanno errori nell'utilizzo del Template:Portale\n\n"
	output += "\n=== {{subst:LOCALDAY}} {{subst:LOCALMONTHNAME}} {{subst:LOCALYEAR}} ===\n"
	for elem in errorPages :
		# Valori per error: redirect, notfound, multiple
		title = elem[0]
		error = elem[1]
		if error == 'redirect' :
			errorMsg = 'è un redirect'
		elif error == 'notfound' :
			errorMsg = 'non ha il template'
		elif error == 'multiple' :
			errorMsg = 'ha più di un template'
		output += "* [[" + title + "]] " + errorMsg + "\n"
	savePage(wikiPage, output, "[[WP:Bot|Bot]]: Registrazione log")

############### STARTING POINT FOR THE SCRIPT ################
print("---- Esecuzione del " + time.strftime("%c") + " ----")

savedContinueFileName = os.environ['ITWIKI_PYWIKIBOT_CONTINUE_TOKEN_FILE']
if not savedContinueFileName :
	print("Environment variable ITWIKI_PYWIKIBOT_CONTINUE_TOKEN_FILE not set. Quitting.")
	sys.exit( 1 )

# Load 'continue string' if it is saved
if os.path.exists( savedContinueFileName ) :
	savedContinueFile = open( savedContinueFileName, 'r' )
	continueStr = savedContinueFile.readline()
else :
	continueStr = ''

# Override page limit if necessary (first parameter of the script)
try:
    LIMIT_TEMPLATE_CHECK = int(sys.argv[1])
except IndexError:
    # no change is needed
    pass

continueFetching = True
#### STARTING MAIN LOOP
while( continueFetching and examinedPages < LIMIT_TEMPLATE_CHECK ):
	# If the continueStr is empty do not append anything
	appendContinue = "&" + URL_CONTINUE + "=" + continueStr if continueStr else ""
	# Get json data
	urlContinued = URL + appendContinue
	jsonData = getJsonFromURL( urlContinued )
	numRequests += 1
	
	if not 'query' in jsonData :
		print('Error detected while parsing XML. Showing erroneus data and quitting.')
		pprint( jsonData )
		sys.exit( 1 )
	# Fetch new continue token, used for next iteration (or being saved)
	if 'query-continue' in jsonData :
		continueStr = jsonData['query-continue']['embeddedin']['eicontinue']
	else :
		print('Query-continue parameter not received. Processing last pages.')
		continueFetching = False

	pageList = getListPage( jsonData['query']['embeddedin'] )

	# Check how many pages we have received
	numPages = len( pageList )
	if continueFetching and numPages != LIMIT_PAGES :
		print(( "Requested " + str( LIMIT_PAGES ) + " pages but " + str( numPages ) + " given. "
			+ "Quitting after next iteration." ))
		continueFetching = False
	
	# Show info every 5 requests
	if numRequests % 5 == 0 :
		print(( str( examinedPages ) + " cont:" + continueStr +
			" error:" + str( error ) + " noSort:" + str( noSortingNeeded ) +
			" alrdSort:" + str( alreadySorted ) + " nextPage:" + pageList[0] )) 
		sys.stdout.flush()
	
	for page in pageList:
		# Let's increment here because of 'continue branches'
		examinedPages += 1

		text = getPageText( page )
		if not text:
			print(( "Skipping page '" + page +
				"'. It's redirect or some error occured." ))
			errorList.append( [ page, 'redirect' ] )
			error += 1
			continue

		result = REGEX_COMPILED.search( text )
		if not result :
			print("Skipping page '" + page + "'. Template not found.")
			errorList.append( [ page, 'notfound' ] )
			error += 1
			continue
		# Get first matched template
		templateStr = result.group()
		arguments = getPortalArguments( templateStr )
		# Check that exactly one template is matching our regex
		matchesList = REGEX_COMPILED.findall( text )
		if len( matchesList ) != 1 :
			# Check whether this is a legal use of multiple templates
			# Multiple templates should be consecutive (separated by spaces or new lines)
			# The first template should contain 5 or 6 arguments.
			multilineRegex = REGEX + ( r'[ \n]*' + REGEX ) * ( len( matchesList ) - 1 )
			multilineMatches = re.findall( multilineRegex, text )
			if len( arguments ) in [5, 6] and len ( multilineMatches ) == 1 :
				print("Skipping page '" + page + "'. Multitemplate used correctly.")
			else :
				print("Skipping page '" + page + "'. Multitemplate not used correctly.")
				errorList.append( [ page, 'multiple' ] )
				error += 1
			continue
		if not arguments:
			print("Some unexpected fatal error occured. Page: " + page)
			sys.exit( 1 )
		forced = editForced( templateStr )
		if not forced and len( arguments ) == 1 :
			# Nothing to sort
			noSortingNeeded += 1
			continue
		argumentsSorted = sorted( arguments, key = str.lower )
		if not forced and argumentsSorted == arguments :
			# Already sorted
			alreadySorted += 1
			continue

		# Arguments not sorted
		# Replace template with new one
		newTemplate = generatePortal( argumentsSorted )
		newText = REGEX_COMPILED.sub( newTemplate, text )
		print("Fixing '" + page + "'")
		sys.stdout.flush()
		putPageText( page, newText )

# Print last status before quitting
print(( str( examinedPages ) + " cont:" + continueStr +
	" error:" + str( error ) + " noSort:" + str( noSortingNeeded ) +
	" alrdSort:" + str( alreadySorted ) ))

# Save 'continue string' to file
print("Saving continue string...")
savedContinueFile = open( savedContinueFileName, 'w' )
savedContinueFile.write( continueStr )

print("Saving error log into " + ERROR_LOG_PAGE + "...")
saveErrorLog( errorList, ERROR_LOG_PAGE )

print("---- Esecuzione terminata: " + time.strftime("%c") + " ----\n")
