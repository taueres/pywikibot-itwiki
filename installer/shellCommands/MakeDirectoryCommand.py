from BaseCommand import BaseCommand

class MakeDirectoryCommand(BaseCommand):
    def __init__(self, directory):
        super(MakeDirectoryCommand, self).__init__(
            'mkdir -p ' + directory,
            None
        )
