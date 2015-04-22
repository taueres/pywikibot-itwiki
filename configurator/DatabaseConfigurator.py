import os.path

class DatabaseConfigurator(object):
    def __init__(self, custom_script_dir):
        self._database_dir = os.path.join(custom_script_dir, 'database')

    def is_configured(self):
        return os.path.isfile(
            os.path.join(self._database_dir, 'DbSettings.py')
        )

    def configure(self):
        username = input('Username for mysql database: ')
        password = input('Password for mysql database: ')
        database = input('Database name for mysql: ')
        host = input('Host for mysql: [127.0.0.1] ')
        if not host:
            host = '127.0.0.1'
        config = {
            'user': username,
            'password': password,
            'host': host,
            'database': database
        }
        self._save_config_to_file(config)

    def _save_config_to_file(self, config):
        f = open(os.path.join(self._database_dir, 'DbSettings.py'), 'w')
        f.write('connection_data = ' + repr(config))
        f.close()

    def get_name(self):
        return 'Database'