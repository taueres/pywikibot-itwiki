import time
import os
import re
import pywikibot
from utils.network import fetch_url_resource
from scripts.BaseScript import BaseScript

REGEX = r"\| ?\[\[:([a-z]+):(?:.|\n)*?'''([0-9,]+)'''"

class UpdateLanguageCounters(BaseScript):

    def execute(self):
        ## Check template has not been modified ##
        wiki_site = pywikibot.Site()
        template = pywikibot.Page(wiki_site, self.settings.get_language_template_page_title())
        latest_revision = template.latestRevision()
        revision_file_name = self.settings.get_language_counters_revision_file_name()
        if os.path.exists(revision_file_name):
            revision_file = open(revision_file_name, 'r')
            revision_stored = revision_file.readline()
            if revision_stored != str(latest_revision):
                return False
        else:
            revision_file = open(revision_file_name, 'w')
            revision_file.write(str(latest_revision))

        counters_data = fetch_url_resource(self.settings.get_language_counters_resource_url())

        matches = re.findall(REGEX, counters_data)
        output = "{{subst:" + self.settings.get_language_template_page_title() + "|"
        if time.localtime().tm_mday in [8, 11]:
            output += "all'"
        else:
            output += "al "
        output += "{{subst:LOCALDAY}} {{subst:LOCALMONTHNAME}} {{subst:LOCALYEAR}}"
        language_iso_to_label = self.settings.get_language_iso_to_label()
        for index in range(10):
            lang, count = matches[index]
            if lang == "it":
                lang = "'''Italiano'''"
                count = "{{NUMBEROFARTICLES}}"
            else:
                lang = "[[:" + lang + ":|" + language_iso_to_label[lang] + "]]"
                count = count.replace(',', '.') + '+'
            output += "|" + lang + "|" + count

        output += "}}<noinclude>[[Categoria:Template pagina principale|Lingue]]</noinclude>"

        wiki_page = pywikibot.Page(wiki_site, "Template:Pagina principale/Lingue")
        self.page_saver.save_page(wiki_page, output, "[[WP:BOT|Bot]]: Aggiornamento")
        return True
