import mysql.connector
import datetime
import os
import json

class LogRecord(object):
    def __init__(self):
        self._command = None
        self._exit_code = None
        self._log_text = None
        self._connection = None

    def set_command(self, command):
        self._command = command

    def set_exit_code(self, exit_code):
        self._exit_code = exit_code

    def set_log_text_from_file(self, file_name):
        with open(file_name, 'r') as f:
            self._log_text = f.read()

    def save(self):
        connection = self._get_connection()
        cursor = connection.cursor()
        sql_log = """
            INSERT INTO log
            (command, exit_code, created_at)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_log, [self._command, self._exit_code, datetime.datetime.now()])
        id_log = cursor.lastrowid
        sql_log_text = """
            INSERT INTO log_text
            (log_id, text)
            VALUES (%s, %s)
        """
        cursor.execute(sql_log_text, [id_log, self._log_text])
        connection.commit()
        cursor.close()
        connection.close()

    def _get_connection(self):
        if not self._connection:
            connection_config = self._get_connection_config()
            self._connection = mysql.connector.connect(**connection_config)

        return self._connection

    def _get_connection_config(self):
        config_file = os.environ.get('ITWIKI_PYWIKIBOT_DATABASE_CONFIG_FILE', None)
        if not config_file:
            raise EnvironmentError('Database config file env var is missing!')

        with open(config_file, 'r') as f:
            return json.load(f)
