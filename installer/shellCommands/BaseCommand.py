class BaseCommand(object):
    def __init__(self, shell_command, rollback_command):
        self._shell_command = shell_command
        self._rollback_command = rollback_command
        self._ignore_errors = False

    def _do_execute(self, command):
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        if 0 != process.returncode and not self._ignore_errors:
            raise RuntimeError('Failed to execute command...')
        return output

    def execute(self):
        return self._do_execute(self._shell_command)

    def rollback(self):
        if self._rollback_command:
            try:
                return self._do_execute(self._rollback_command)
            except Exception:
                pass

    def ignore_errors(self, do_ignore):
        self._ignore_errors = do_ignore