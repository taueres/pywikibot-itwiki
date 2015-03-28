from shellCommands.MakeDirectoryCommand import MakeDirectoryCommand
from shellCommands.GitCloneCommand import GitCloneCommand
from shellCommands.CommandContext import CommandContext

PYWIKIBOT_REPOSITORY_URI = 'https://github.com/wikimedia/pywikibot-core.git'

class PywikibotInstaller(object):
    def __init__(self):
        self._command_context = CommandContext()
        self._install_directory = None

    def install(self):
        default_dir = self._get_recommended_dir()
        print 'Where should I install pywikibot? [' + default_dir + ']'
        directory = raw_input()
        if not directory:
            print 'Using default directory...'
            directory = default_dir

        print 'Creating directory...'
        make_directory = MakeDirectoryCommand(directory)
        if not self._execute_command(make_directory):
            return False

        print 'Downloading pywikibot...'
        git_clone = GitCloneCommand(PYWIKIBOT_REPOSITORY_URI, directory)
        if not self._execute_command(git_clone):
            return False

        self._install_directory = directory
        print 'Pywikibot installed correctly!'
        return True

    def _get_recommended_dir(self):
        from os.path import dirname, realpath, join
        base_path = dirname(dirname(dirname(realpath(__file__))))
        return join(base_path, 'core')

    def _execute_command(self, command):
        try:
            self._command_context.execute_command(command)
            return True
        except Exception:
            self._command_context.rollback_commands()
            return False

    def get_install_path(self):
        return self._install_directory