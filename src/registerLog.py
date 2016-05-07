import sys
from database.LogRecord import LogRecord

command = sys.argv[1]
exit_code = sys.argv[2]
log_file = sys.argv[3]

record = LogRecord()
record.set_command(command)
record.set_exit_code(exit_code)
record.set_log_text_from_file(log_file)

record.save()
