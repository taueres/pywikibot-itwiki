from installer.PywikibotInstaller import PywikibotInstaller
from configurator.PywikibotConfigurator import PywikibotConfigurator

def yesNoQuestion(question):
    question += ' Y/N: '
    return raw_input(question) in ['y', 'yes', 'Y', 'YES']

# PYWIKIBOT INSTALL
pywikibot_installed = yesNoQuestion("Pywikibot is already installed?")
if pywikibot_installed:
    pywikibot_dir = raw_input("Directory of pywikibot: ")
else:
    installer = PywikibotInstaller()
    if not installer.install():
        print 'Error installing pywikibot. Aborting...'
        exit(1)
    pywikibot_dir = installer.get_install_path()

# PYWIKIBOT CONFIGURATION
configurator = PywikibotConfigurator(pywikibot_dir)
if configurator.is_configured():
    print 'Pywikibot is configured'
else:
    print 'Configuring Pywikibot...'
    configurator.configure()
    if not configurator.is_configured():
        print 'Configuration failed. Aborting...'
        exit(1)

