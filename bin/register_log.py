def main(argv):
    command = argv[1]
    exit_code = argv[2]
    log_file = argv[3]

    import os
    from config.Settings import Settings

    settings = Settings(os.environ)
    if settings.is_debug():
        print('Debug mode detected. Writing to stdout instead of database.')
        with open(log_file) as fh:
            print(fh.read())
        return 0

    from database.LogRecord import LogRecord
    record = LogRecord()
    record.set_command(command)
    record.set_exit_code(exit_code)
    record.set_log_text_from_file(log_file)

    record.save()
    return 0

if __name__ == '__main__':
    import sys
    sys.path[0] = '/root/it-pywikibot/src'
    exit_code = main(sys.argv)
    sys.exit(exit_code)
