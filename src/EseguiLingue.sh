#!/bin/bash
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "---- Esecuzione del "$(date)" ----"
if [ -e "$ITWIKI_PYWIKIBOT_LANGUAGE_FILE" ]
  then
    rm "$ITWIKI_PYWIKIBOT_LANGUAGE_FILE"
fi
wget -q -O "$ITWIKI_PYWIKIBOT_LANGUAGE_FILE" "https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table?action=raw"
exit_code=$?
if [ ${exit_code} != 0 ]; then
    echo "Error while downloading languages data. Quitting."
    exit ${exit_code}
fi
python ${CURRENT_SCRIPT_DIR}/AltreLingue.py
