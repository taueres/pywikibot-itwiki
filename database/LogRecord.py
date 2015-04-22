import mysql.connector
import datetime
from . import DbSettings

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
        f = open(file_name, 'r')
        self._log_text = f.read()
        f.close()

    def save(self):
        cursor = self._get_connection().cursor()
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
        self._get_connection().commit()
        cursor.close()
        self._get_connection().close()

    def _get_connection(self):
        if not self._connection:
            self._connection = mysql.connector.connect(**DbSettings.connection_data)
        return self._connection