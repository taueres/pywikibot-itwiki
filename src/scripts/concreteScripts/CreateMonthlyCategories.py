from scripts.BaseScript import BaseScript
import time
import pywikibot

class CreateMonthlyCategories(BaseScript):

    def __init__(self, settings, page_saver):
        super().__init__(settings, page_saver)
        self.wiki_site = pywikibot.getSite()
        self.subject = "[[WP:Bot|Bot]]: Creazione categoria mensile"

    def create_category(self, title, content):
        page = pywikibot.Page(self.wiki_site, title)
        if not page.exists():
            self.page_saver.save_page(page, content, self.subject, strip_leading_spaces = True)
        else:
            print('{0} already exists.'.format(title))

    def execute(self):
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

        if not (day in range(27, 32)) and not self.settings.is_debug():
          print('Cannot run the job at this day of the month! Day detected: ' + str(day))
          return False

        monthName = self.settings.get_month_names()[strMonth]
        categories_list=[
            "Categoria:Aiutare - " + monthName + " " + year,
            "Categoria:Controllare - "+ monthName + " " + year,
            "Categoria:Controllare copyright - " + monthName + " " + year,
            "Categoria:Verificare enciclopedicità - " + monthName + " " + year,
            "Categoria:Senza fonti - " + monthName + " " + year,
            "Categoria:Contestualizzare fonti - " + monthName + " " + year,
            "Categoria:Localismo - " + monthName + " " + year,
            "Categoria:Pagine orfane - " + monthName + " " + year,
            "Categoria:Voci non neutrali - " + monthName + " " + year,
            "Categoria:Tradurre - " + monthName + " " + year,
            "Categoria:Unire - " + monthName + " " + year,
            "Categoria:Wikificare - " + monthName + " " + year,
            "Categoria:Correggere - " + monthName + " " + year,
            "Categoria:Lavoro sporco - " + monthName + " " + year,
            "Categoria:Voci monitorate - " + monthName + " " + year,
            "Categoria:Voci entrate in vetrina nel mese di " + monthName + " " + year,
            "Categoria:Voci di qualità valutate nel mese di " + monthName + " " + year
        ]

        print('Creating monthly maintenance categories')
        dynamic_snippets = self.settings.get_dynamic_category_snippets()
        for i in range(13):
            page_text = """__HIDDENCAT__
            {{categoria lavoro|""" + dynamic_snippets[i][0] + "|data=" + monthName + " " + year + """}}
            {{Indice categoria}}\n
            [[Categoria:""" + dynamic_snippets[i][1] + "| " + year + " " + strMonth + """]]
            [[Categoria:Lavoro sporco - """ + monthName + " " + year + "|" + dynamic_snippets[i][2] + "]]"
            self.create_category(categories_list[i], page_text)

        ## Main category LAVORO SPORCO
        page_text = "Questa categoria serve per coordinare il [[Aiuto:Lavoro sporco|lavoro sporco]] nel mese di " + monthName + " " + year + """.\n
        [[Categoria:Lavoro sporco per mese| """ + year + " " + strMonth + "]]"
        self.create_category(categories_list[13], page_text)

        categories_content_text = {
            14: "[[Categoria:Voci monitorate per mese| " + year + " " + strMonth + "]]",
            15: "Questa categoria comprende le voci entrate in vetrina nel corso del mese di " + monthName + " " + year + """.
                __HIDDENCAT__\n
                [[Categoria:Voci in vetrina per mese| """ + year + " " + strMonth + "]]",
            16: "Questa categoria comprende le voci riconosciute di qualità nel corso del mese di " + monthName + " " + year + """.
                __HIDDENCAT__\n
                [[Categoria:Voci di qualità per mese| """ + year + " " + strMonth + "]]"
        }

        for i in range(14, 17):
            self.create_category(categories_list[i], categories_content_text[i])

        return True
