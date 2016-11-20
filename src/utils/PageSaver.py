class PageSaver(object):
    def __init__(self, settings):
        self.settings = settings

    def save_page(self, page, text, summary, strip_leading_spaces = False):
        if strip_leading_spaces:
            text = '\n'.join(map(lambda x: x.lstrip(' '), text.split('\n')))

        if self.settings.is_debug():
            print('******* Writing to page: "' + page.title() + '" *******')
            print('Summary: "' + summary + '"')
            print('BEGIN text')
            print(text)
            print('END text')
        else:
            page.put(text, summary)
