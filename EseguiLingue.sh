#!/bin/bash
echo "---- Esecuzione del "$(date)" ----"
if [ -e "$DATI_LINGUE_FILE" ]
  then
    rm "$DATI_LINGUE_FILE"
fi
wget -q -O "$DATI_LINGUE_FILE" "https://meta.wikimedia.org/wiki/List_of_Wikipedias/Table?action=raw"
exit_code=$?
if [ $exit_code != 0 ]; then
	echo "Error while downloading languages data. Quitting."
	exit $exit_code
fi
python $CUSTOM_SCRIPTS_DIR/AltreLingue.py
