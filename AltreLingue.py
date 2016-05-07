# -*- coding: utf-8 -*-
#
#   (c) 2010 Santoro Sergio
#   Questo programma è software libero: puoi ridistribuirlo e/o modificarlo
#   rispettando i termini della GNU General Public License pubblicata dalla
#   Free Software Foundation, versione 3 o successive.
#
#   Questo programma è distribuito nella speranza che possa essere
#   utile, ma SENZA ALCUNA GARANZIA; senza neppure la garanzia
#   implicita di COMMERCIABILITA' o IDONEITA' PER UN PARTICOLARE SCOPO.
#   Per maggiori informazioni vedere la licenza completa su:
#   http://www.gnu.org/licenses/

import sys, time, os, re
import pywikibot
from settings import savePage, CODICI_LINGUE, TEMPLATE_BOT

REGEX = r"\| ?\[\[:([a-z]+):(?:.|\n)*?'''([0-9,]+)'''"

## Check template has not been modified ##
wikiSite = pywikibot.Site()
template = pywikibot.Page(wikiSite, TEMPLATE_BOT)
actualRevision = template.latestRevision()
if os.path.exists(os.environ['ITWIKI_PYWIKIBOT_REVISION_FILE']):
    revFile = open(os.environ['ITWIKI_PYWIKIBOT_REVISION_FILE'], 'r')
    revStored = revFile.readline()
    if revStored != str(actualRevision):
        email_text="""From: $SERVER_NAME <$SERVER_EMAIL>
To: Administrator <$ADMIN_EMAIL>
Subject: Error with AltreLingue.py
Content-Type: text/plain

Bot template modified. Execution interrupted.
Please check whether the edit is okay and delete SavedRevisionNumber file."""
        os.system( "echo -e \"" + email_text + "\" | sendmail $ADMIN_EMAIL" )
        sys.exit( 1 )
else:
    revFile = open(os.environ['ITWIKI_PYWIKIBOT_REVISION_FILE'], 'w')
    revFile.write(str(actualRevision))

document = open(os.environ['ITWIKI_PYWIKIBOT_LANGUAGE_FILE'], 'r')
text = document.read()
matches = re.findall(REGEX, text)
output = "{{subst:" + TEMPLATE_BOT + "|"
if time.localtime().tm_mday in [8,11]:
    output += "all'"
else:
    output += "al "
output += "{{subst:LOCALDAY}} {{subst:LOCALMONTHNAME}} {{subst:LOCALYEAR}}"
for index in range(10):
    lang, count = matches[index]
    if lang == "it":
        lang = "'''Italiano'''"
        count = "{{NUMBEROFARTICLES}}"
    else:
        lang = "[[:" + lang + ":|" + CODICI_LINGUE[lang] + "]]"
        count = count.replace( ',', '.' ) + '+'
    output += "|" + lang + "|" + count

output += "}}<noinclude>[[Categoria:Template pagina principale|Lingue]]</noinclude>"

wikiPage = pywikibot.Page(wikiSite, "Template:Pagina principale/Lingue")
savePage(wikiPage, output, "[[WP:BOT|Bot]]: Aggiornamento")
print('---- Esecuzione terminata ----\n')
