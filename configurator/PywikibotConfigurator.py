import os.path

class PywikibotConfigurator(object):
    def __init__(self, pywikibot_dir):
        self._pywikibot_dir = pywikibot_dir

    def is_configured(self):
        return os.path.isfile(self._get_config_file_name())

    def configure(self):
        import imp, sys
        sys.path.append(self._pywikibot_dir)
        pywb_module = imp.load_source(
            'generate_user_files',
            os.path.join(self._pywikibot_dir, 'generate_user_files.py')
        )
        pywb_module.base_dir = self._pywikibot_dir
        pywb_module.create_user_config()

        username = raw_input('Pywikibot username: ')
        password = raw_input('Pywikibot password: ')
        saved_file = self._save_username_and_password(username, password)

        config_file = self._get_config_file_name()
        config_file_handler = open(config_file, 'a')
        config_file_handler.write('password_file = "' + saved_file + '"\n')
        config_file_handler.close()

    def _get_config_file_name(self):
        return os.path.join(self._pywikibot_dir, 'user-config.py')

    def _save_username_and_password(self, username, password):
        import stat
        destination_file = os.path.join(self._pywikibot_dir, 'login-data')
        file_data = open(destination_file, 'w')
        file_data.write("('" + username + "','" + password + "')\n")
        file_data.close()
        os.chmod(destination_file, stat.S_IREAD)

        return destination_file