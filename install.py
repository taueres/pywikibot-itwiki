from installer.PywikibotInstaller import PywikibotInstaller
from configurator.PywikibotConfigurator import PywikibotConfigurator
from configurator.EnvironmentConfigurator import EnvironmentConfigurator
from configurator.DatabaseConfigurator import DatabaseConfigurator
import os.path

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
custom_dir = os.path.dirname(os.path.realpath(__file__))
configurators = [
    PywikibotConfigurator(pywikibot_dir),
    EnvironmentConfigurator(pywikibot_dir, custom_dir),
    DatabaseConfigurator(custom_dir)
]
for configurator in configurators:
    if configurator.is_configured():
        print configurator.get_name() + ' is configured'
    else:
        print 'Configuring ' + configurator.get_name() + '...'
        configurator.configure()
        if not configurator.is_configured():
            print 'Configuration failed. Aborting...'
            exit(1)
# TODO: apply default schema to database
print 'Installer finished successfully!'