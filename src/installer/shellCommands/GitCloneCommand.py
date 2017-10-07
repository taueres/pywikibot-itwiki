from .BaseCommand import BaseCommand

class GitCloneCommand(BaseCommand):
    def __init__(self, repository_uri, directory):
        super(GitCloneCommand, self).__init__(
            'git clone ' + repository_uri + ' ' + directory,
            'rm -rf ' + directory
        )
