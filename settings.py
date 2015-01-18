# -*- coding: utf-8 -*-

## COMUNE A TUTTI GLI SCRIPT

#DEBUG_MODE = True
DEBUG_MODE = False

def savePage(page, text, summary):
  if DEBUG_MODE:
    print u'******* Scrittura su pagina: "'.encode('utf-8') + page.title().encode('utf-8') + u'" ('.encode('utf-8') + summary.encode('utf-8') + u'):'.encode('utf-8')
    print text.encode('utf-8')
  else:
    page.put(text, summary)

## SEZIONE PER ALTRE_LINGUE

CODICI_LINGUE = {
 "en": "English (''inglese'')",
 "de": "Deutsch (''tedesco'')",
 "fr": u"Français (''francese'')",
 "pl": "Polski (''polacco'')",
 "it": "'''Italiano'''",
 "ja": u"日本語 (''giapponese'')",
 "es": u"Español (''spagnolo'')",
 "pt": u"Português (''portoghese'')",
 "nl": "Nederlands (''olandese'')",
 "ru": u"Русский (''russo'')",
 "sv": "Svenska (''svedese'')",
 "zh": u"中文 (''cinese'')",
 "war": u"Winaray (''waray'')",
 "vi": u"Tiếng Việt (''vietnamita'')",
 "ceb": u"Binisaya (''cebuano'')"
}

TEMPLATE_BOT = "Utente:TauerBot/tmp"

## SEZIONE PER CATEGORIE_MENSILI

TESTO_DINAMICO = [
["A","Aiutare per mese","Aiutare"],
["C","Controllare per mese","Controllare"],
["Controlcopy","Controllare copyright per mese","Controllare copyright"],
["E",u"Verificare enciclopedicità per mese",u"Enciclopedicità"],
["F","Senza fonti per mese","Fonti"],
["NN","Contestualizzare fonti per mese","Fonti non contestualizzate"],
["L","Localismo per mese","Localismo"],
["O","Pagine orfane per mese","Orfane"],
["P","Voci non neutrali per mese","POV"],
["T","Tradurre per mese","Tradurre"],
["U","Unire per mese","Unire"],
["W","Wikificare per mese","Wikificare"],
["Correggere","Correggere per mese","Correggere"]
]

NOMI_MESI = {
"01":"gennaio",
"02":"febbraio",
"03":"marzo",
"04":"aprile",
"05":"maggio",
"06":"giugno",
"07":"luglio",
"08":"agosto",
"09":"settembre",
"10":"ottobre",
"11":"novembre",
"12":"dicembre"
}

## SEZIONE PER ROTAZIONE LOG
MAX_LOG_SIZE = 12 * 1024 # 12 Kilobyte

## SEZIONE PER AGGIORNAMENTO PORTALE
LIMIT_TEMPLATE_CHECK = 60000
