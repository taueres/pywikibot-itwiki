class CommandContext(object):
    def __init__(self):
        self._commands = []

    def execute_command(self, command):
        self._commands.insert(0, command)
        command.execute()

    def rollback_commands(self):
        for command in self._commands:
            command.rollback()