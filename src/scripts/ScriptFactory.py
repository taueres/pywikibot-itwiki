
class ScriptFactory(object):

    def __init__(self, settings, page_saver):
        self.settings = settings
        self.page_saver = page_saver

    def build_script(self, command_name):
        if command_name == 'language-counters':
            from scripts.concreteScripts.UpdateLanguageCounters import UpdateLanguageCounters
            return UpdateLanguageCounters(self.settings, self.page_saver)

        elif command_name == 'monthly-categories':
            from scripts.concreteScripts.CreateMonthlyCategories import CreateMonthlyCategories
            return CreateMonthlyCategories(self.settings, self.page_saver)

        elif command_name == 'portale-template':
            from scripts.concreteScripts.FixPortaleTemplate import FixPortaleTemplate
            return FixPortaleTemplate(self.settings, self.page_saver)

        else:
            raise RuntimeError('The requested command "' + command_name + '" is unknown')
