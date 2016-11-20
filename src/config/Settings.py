import os

URL_LANGUAGE_COUNTERS = "https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table?action=raw"
TEMPLATE_BOT = "Utente:TauerBot/tmp"

LANGUAGE_ISO_TO_LABEL = {
 "en": "English (''inglese'')",
 "de": "Deutsch (''tedesco'')",
 "fr": "Français (''francese'')",
 "pl": "Polski (''polacco'')",
 "it": "'''Italiano'''",
 "ja": "日本語 (''giapponese'')",
 "es": "Español (''spagnolo'')",
 "pt": "Português (''portoghese'')",
 "nl": "Nederlands (''olandese'')",
 "ru": "Русский (''russo'')",
 "sv": "Svenska (''svedese'')",
 "zh": "中文 (''cinese'')",
 "war": "Winaray (''waray'')",
 "vi": "Tiếng Việt (''vietnamita'')",
 "ceb": "Binisaya (''cebuano'')"
}

ITALIAN_MONTH_NAMES = {
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

DYNAMIC_CATEGORY_SNIPPETS = [
    ["A","Aiutare per mese","Aiutare"],
    ["C","Controllare per mese","Controllare"],
    ["Controlcopy","Controllare copyright per mese","Controllare copyright"],
    ["E","Verificare enciclopedicità per mese","Enciclopedicità"],
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

class Settings:

    def __init__(self, environ):
        self.environ = environ

    def is_debug(self):
        return bool(self.environ.get('TAUERBOT_DEBUG', False))

    def get_language_counters_storage_file_name(self):
        return self.environ.get('TAUERBOT_LANGUAGE_FILE')

    def get_language_counters_resource_url(self):
        return URL_LANGUAGE_COUNTERS

    def get_language_counters_revision_file_name(self):
        return self.environ.get('TAUERBOT_REVISION_FILE')

    def get_language_template_page_title(self):
        return TEMPLATE_BOT

    def get_language_iso_to_label(self):
        return LANGUAGE_ISO_TO_LABEL

    def get_month_names(self):
        return ITALIAN_MONTH_NAMES

    def get_dynamic_category_snippets(self):
        return DYNAMIC_CATEGORY_SNIPPETS

    def get_portale_continue_token_file(self):
        return self.environ['TAUERBOT_CONTINUE_TOKEN_FILE']

## SEZIONE PER ROTAZIONE LOG
MAX_LOG_SIZE = 12 * 1024 # 12 Kilobyte

## SEZIONE PER AGGIORNAMENTO PORTALE
LIMIT_TEMPLATE_CHECK = 60000
