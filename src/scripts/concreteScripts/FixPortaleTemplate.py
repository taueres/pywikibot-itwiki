from scripts.BaseScript import BaseScript

import json
import urllib.request, urllib.error, urllib.parse, os, sys, time
import pywikibot, re
from pprint import pprint
import requests

# Constants
SUMMARY = "[[WP:Bot|Bot]]: Fix portali in ordine alfabetico"
REGEX = r'\{\{[ \n]*([Tt]emplate: *)?([Pp]ortale|[Pp]rogetto|[Pp]ortali)[ \n]*\|[^\{\}]*\}\}'
REGEX_COMPILED = re.compile(REGEX)
TEMPLATE = "Template:Portale"
LIMIT_PAGES = 100
URL = ("https://it.wikipedia.org/w/api.php?action=query&list=embeddedin&eititle=" + TEMPLATE +
       "&einamespace=0&eilimit=" + str(LIMIT_PAGES) + "&format=json")
URL_CONTINUE = "eicontinue"
ERROR_LOG_PAGE = "Utente:TauerBot/Portale"

def getJsonFromURL(url):
    response = requests.get(url)
    jsonData = json.loads(response.text)
    return jsonData

def getListPage(page_list):
    return list(map(lambda x: x['title'], page_list))

def getPortalArguments(portalTemplate):
    output = portalTemplate.split('|')
    output.pop(0) # Take away the template itself
    lastIndex = len(output) - 1

    if lastIndex < 0:
        # Empty list?
        # This shouldn't happen (see regex we used)
        return False

    if '}}' not in output[lastIndex]:
        # Template is not closed
        # This shouldn't happen (see regex we used)
        return False

    # Remove }} closing template from the last element
    output[lastIndex] = output[lastIndex].replace('}}', '')

    # Strip leading and trailing spaces
    # Removing empty arguments
    delIndex = []
    for (i, elem) in enumerate(output):
        output[i] = elem.strip()
        if not output[i]:
            delIndex.append(i)
    # Set delIndex in descending order: pop will overwrite the indexes
    delIndex.reverse()
    for ind in delIndex:
        output.pop(ind)
    return output

def generatePortal(arguments):
    output = "{{Portale"
    for argument in arguments:
        output += '|' + argument
    output += '}}'
    return output

# Force edit when empty arguments are present or template Progetto is used
def editForced(portalTemplate):
    rawArgs = portalTemplate.split('|')
    for arg in rawArgs:
        if not arg:
            return True
    if 'progetto' in rawArgs[0].lower():
        return True
    if 'portali' in rawArgs[0].lower():
        return True
    if 'template' in rawArgs[0].lower():
        return True
    if '\n' in rawArgs[0]:
        return True
    return False

def saveErrorLog(errorPages, wikiPageTitle):
    if len(errorPages) == 0:
        return
    wikiPage = pywikibot.Page(wikiSite, wikiPageTitle)
    if not wikiPage:
        raise Exception('Error while getting wikiPageTitle')
    if wikiPage.exists():
        output = wikiPage.get()
    else:
        output = "In questa pagina vengono elencate le voci che hanno errori nell'utilizzo del Template:Portale\n\n"
    output += "\n=== {{subst:LOCALDAY}} {{subst:LOCALMONTHNAME}} {{subst:LOCALYEAR}} ===\n"
    for elem in errorPages:
        # Valori per error: redirect, notfound, multiple
        title = elem[0]
        error = elem[1]
        if error == 'redirect':
            errorMsg = 'è un redirect'
        elif error == 'notfound':
            errorMsg = 'non ha il template'
        elif error == 'multiple':
            errorMsg = 'ha più di un template'
        output += "* [[" + title + "]] " + errorMsg + "\n"
    savePage(wikiPage, output, "[[WP:Bot|Bot]]: Registrazione log")

class FixPortaleTemplate(BaseScript):
    def __init__(self, *args):
        super().__init__(*args)

        self.wikiSite = pywikibot.getSite()
        self.errorList = []

        ## Start counters
        self.examinedPages = 0
        self.numRequests = 0
        self.error = 0
        self.noSortingNeeded = 0
        self.alreadySorted = 0
        ## End counters

    def execute(self):
        savedContinueFileName = self.settings.get_portale_continue_token_file()
        if not savedContinueFileName :
            print("Environment variable TAUERBOT_CONTINUE_TOKEN_FILE not set. Quitting.")
            sys.exit(1)

        # Load 'continue string' if it is saved
        if os.path.exists(savedContinueFileName):
            with open(savedContinueFileName, 'r') as savedContinueFile:
                continueStr = savedContinueFile.readline()
        else:
            continueStr = ''

        # Override page limit if necessary (first parameter of the script)
        try:
            LIMIT_TEMPLATE_CHECK = int(sys.argv[2])
        except IndexError:
            LIMIT_TEMPLATE_CHECK = 6000
            pass

        continueFetching = True
        #### STARTING MAIN LOOP
        while(continueFetching and self.examinedPages < LIMIT_TEMPLATE_CHECK):
            # If the continueStr is empty do not append anything
            appendContinue = "&" + URL_CONTINUE + "=" + continueStr if continueStr else ""
            # Get json data
            urlContinued = URL + appendContinue
            jsonData = getJsonFromURL(urlContinued)
            self.numRequests += 1

            if not 'query' in jsonData :
                print('Error detected while parsing JSON response. Showing erroneus data and quitting.')
                pprint(jsonData)
                sys.exit(1)
            # Fetch new continue token, used for next iteration (or being saved)
            if 'continue' in jsonData :
                continueStr = jsonData['continue']['eicontinue']
            else :
                print('Query-continue parameter not received. Processing last pages.')
                continueFetching = False

            pageList = getListPage(jsonData['query']['embeddedin'])

            # Check how many pages we have received
            numPages = len(pageList)
            if continueFetching and numPages != LIMIT_PAGES :
                print(( "Requested " + str( LIMIT_PAGES ) + " pages but " + str( numPages ) + " given. "
                    + "Quitting after next iteration." ))
                continueFetching = False

            # Show info every 5 requests
            if self.numRequests % 5 == 0:
                print((str(self.examinedPages) + " cont:" + continueStr +
                       " error:" + str(self.error) + " noSort:" + str(self.noSortingNeeded) +
                       " alrdSort:" + str(self.alreadySorted) + " nextPage:" + pageList[0]))
                sys.stdout.flush()

            for page in pageList:
                # Let's increment here because of 'continue branches'
                self.examinedPages += 1

                text = self.getPageText(page)
                if not text:
                    print(( "Skipping page '" + page +
                        "'. It's redirect or some error occured." ))
                    self.errorList.append([page, 'redirect'])
                    self.error += 1
                    continue

                result = REGEX_COMPILED.search(text)
                if not result :
                    print("Skipping page '" + page + "'. Template not found.")
                    self.errorList.append( [ page, 'notfound' ] )
                    self.error += 1
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
                        self.errorList.append( [ page, 'multiple' ] )
                        self.error += 1
                    continue
                if not arguments:
                    print("Some unexpected fatal error occured. Page: " + page)
                    sys.exit( 1 )
                forced = editForced( templateStr )
                if not forced and len( arguments ) == 1 :
                    # Nothing to sort
                    self.noSortingNeeded += 1
                    continue
                argumentsSorted = sorted( arguments, key = str.lower )
                if not forced and argumentsSorted == arguments :
                    # Already sorted
                    self.alreadySorted += 1
                    continue

                # Arguments not sorted
                # Replace template with new one
                newTemplate = generatePortal( argumentsSorted )
                newText = REGEX_COMPILED.sub( newTemplate, text )
                print("Fixing '" + page + "'")
                sys.stdout.flush()
                self.putPageText(page, newText)

        # Print last status before quitting
        print(( str( self.examinedPages ) + " cont:" + continueStr +
            " error:" + str(self.error) + " noSort:" + str(self.noSortingNeeded) +
            " alrdSort:" + str(self.alreadySorted) ))

        # Save 'continue string' to file
        print("Saving continue string...")
        with open( savedContinueFileName, 'w' ) as savedContinueFile:
            savedContinueFile.write( continueStr )

        # print("Saving error log into " + ERROR_LOG_PAGE + "...")
        # saveErrorLog( errorList, ERROR_LOG_PAGE )

    def getPageText(self, pageTitle):
        wikiPage = pywikibot.Page(self.wikiSite, pageTitle)
        if not wikiPage:
            return False
        if wikiPage.isRedirectPage():
            return False
        return wikiPage.get()

    def putPageText(self, page_title, text):
        wiki_page = pywikibot.Page(self.wikiSite, page_title)
        self.page_saver.save_page(wiki_page, text, SUMMARY)