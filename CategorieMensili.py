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

import sys, time
import pywikibot
from settings import DEBUG_MODE, savePage, TESTO_DINAMICO, NOMI_MESI

## FOR DEBUGGING
#day = 29
#month = 5
#intYear = 2014

day = time.localtime().tm_mday
month = time.localtime().tm_mon
intYear = time.localtime().tm_year

intYear = intYear + 1 if month == 12 else intYear
month = month % 12 + 1

year = str(intYear)

strMonth = str(month)
strMonth = '0' + strMonth if len(strMonth) == 1 else strMonth

if not (day in range(27, 32)) and not DEBUG_MODE:
  print u'Lasso di tempo non valido per l\'esecuzione. Giorno rilevato: ' + str(day)
  sys.exit( 1 )

Oggetto="[[WP:Bot|Bot]]: Creazione categoria mensile"

monthName = NOMI_MESI[strMonth]
Elenco=[
    u"Categoria:Aiutare - " + monthName + " " + year,
    u"Categoria:Controllare - "+ monthName + " " + year,
    u"Categoria:Controllare copyright - " + monthName + " " + year,
    u"Categoria:Verificare enciclopedicità - " + monthName + " " + year,
    u"Categoria:Senza fonti - " + monthName + " " + year,
    u"Categoria:Contestualizzare fonti - " + monthName + " " + year,
    u"Categoria:Localismo - " + monthName + " " + year,
    u"Categoria:Pagine orfane - " + monthName + " " + year,
    u"Categoria:Voci non neutrali - " + monthName + " " + year,
    u"Categoria:Tradurre - " + monthName + " " + year,
    u"Categoria:Unire - " + monthName + " " + year,
    u"Categoria:Wikificare - " + monthName + " " + year,
    u"Categoria:Correggere - " + monthName + " " + year,
    u"Categoria:Lavoro sporco - " + monthName + " " + year,
    u"Categoria:Voci monitorate - " + monthName + " " + year,
    u"Categoria:Voci entrate in vetrina nel mese di " + monthName + " " + year,
    u"Categoria:Voci di qualità valutate nel mese di " + monthName + " " + year
]

print 'Esecuzione script creazione categorie mensili'
wikiSite = pywikibot.getSite()
##CREAZIONE DELLE CATEGORIE MENSILI
for i in range(13):
  pagina = pywikibot.Page(wikiSite, Elenco[i])
  if not pagina.exists():
    Testo=u"""__HIDDENCAT__
{{categoria lavoro|"""+TESTO_DINAMICO[i][0]+"|data="+monthName+" "+year+u"""}}
{{Indice categoria}}\n
[[Categoria:"""+TESTO_DINAMICO[i][1]+u"| "+year+" "+strMonth+u"""]]
[[Categoria:Lavoro sporco - """+monthName+" "+year+u"|"+TESTO_DINAMICO[i][2]+"]]"
    savePage(pagina, Testo, Oggetto)
  else:
    print u"Pagina ".encode('utf-8') + Elenco[i].encode('utf-8') + u" già esistente.".encode('utf-8')

##CREAZIONE DELLA CATEGORIA RIEPILOGATIVA MENSILE
pagina = pywikibot.Page(wikiSite, Elenco[13])
if not pagina.exists():
  Testo=u"Questa categoria serve per coordinare il [[Aiuto:Lavoro sporco|lavoro sporco]] nel mese di "+monthName+" "+year+u""".\n
[[Categoria:Lavoro sporco per mese| """+year+" "+strMonth+u"]]"
  savePage(pagina, Testo, Oggetto)
else:
  print u'Pagina di riepilogo già esistente.'.encode('utf-8')
##CREAZIONE DELLA CATEGORIA PER LE VOCI MONITORATE
pagina = pywikibot.Page(wikiSite, Elenco[14])
if not pagina.exists():
  Testo=u"[[Categoria:Voci monitorate per mese| "+year+" "+strMonth+u"]]"
  savePage(pagina, Testo, Oggetto)
else:
  print u'Pagina per le voci monitorate già esistente.'.encode('utf-8')
##CREAZIONE DELLA CATEGORIA PER LA VETRINA
pagina = pywikibot.Page(wikiSite, Elenco[15])
if not pagina.exists():
  Testo=u"Questa categoria comprende le voci entrate in vetrina nel corso del mese di "+monthName+" "+year+""".
__HIDDENCAT__\n
[[Categoria:Voci in vetrina per mese| """+year+" "+strMonth+u"]]"
  savePage(pagina, Testo, Oggetto)
else:
  print u'Pagina per la vetrina già esistente.'.encode('utf-8')
##CREAZIONE DELLA CATEGORIA PER LE VOCI DI QUALITÀ
pagina = pywikibot.Page(wikiSite, Elenco[16])
if not pagina.exists():
  Testo=u"Questa categoria comprende le voci riconosciute di qualità nel corso del mese di "+monthName+" "+year+u""".
__HIDDENCAT__\n
[[Categoria:Voci di qualità per mese| """+year+" "+strMonth+u"]]"
  savePage(pagina, Testo, Oggetto)
else:
  print u'Pagina per le voci di qualità già esistente.'.encode('utf-8')
