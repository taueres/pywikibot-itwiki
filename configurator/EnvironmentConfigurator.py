import os.path

class EnvironmentConfigurator(object):
    def __init__(self, pywikibot_dir, custom_script_dir):
        self._pywikibot_dir = pywikibot_dir
        self._custom_script_dir = custom_script_dir

    def is_configured(self):
        return os.path.isfile(
            os.path.join(self._pywikibot_dir, 'user-config.py')
        )

    def configure(self):
        import imp, sys
        sys.path.append(self._pywikibot_dir)
        pywb_module = imp.load_source(
            'generate_user_files',
            os.path.join(self._pywikibot_dir, 'generate_user_files.py')
        )
        pywb_module.base_dir = self._pywikibot_dir
        pywb_module.create_user_config()
