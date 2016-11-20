"""BaseScript abstract class"""

class BaseScript(object):
    """BaseScript abstract class"""

    def __init__(self, settings, page_saver):
        self.settings = settings
        self.page_saver = page_saver

    def execute(self):
        """"Execute this script"""
        raise RuntimeError('Method execute() must be overridden by subclasses')
