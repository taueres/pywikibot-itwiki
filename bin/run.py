def main(argv):
    from scripts.ScriptFactory import ScriptFactory
    from config.Settings import Settings
    from utils.PageSaver import PageSaver
    import os
    import sys

    settings = Settings(os.environ)
    page_saver = PageSaver(settings)

    factory = ScriptFactory(settings, page_saver)
    script = factory.build_script(argv[1])
    is_successful = script.execute()

    if is_successful:
        return 0
    else:
        return 1

if __name__ == '__main__':
    import sys
    sys.path[0] = '/root/it-pywikibot/src'
    exit_code = main(sys.argv)
    sys.exit(exit_code)
