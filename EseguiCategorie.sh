#!/bin/bash
if [ "$MANUAL_MODE" != "yes" ]; then
	YEAR_DIR="$(date +%Y)"
	LOG_FILE_NAME="$(date +%m).log"

	## For debugging
	#YEAR_DIR="2014"
	#LOG_FILE_NAME="04.log"

	DIR_CREATED=""
	if [ ! -d "$LOG_DIR_CATEGORIE/$YEAR_DIR" ]; then
		mkdir "$LOG_DIR_CATEGORIE/$YEAR_DIR"
		DIR_CREATED="yes"
	fi

	# Close STDOUT file descriptor
	exec 1<&-
	# Close STDERR FD
	exec 2<&-
	# Open STDOUT as $LOG_FILE file for read and write.
	exec 1<>$LOG_DIR_CATEGORIE/$YEAR_DIR/$LOG_FILE_NAME
	# Redirect STDERR to STDOUT
	exec 2>&1
fi
echo
echo "---- Esecuzione del "$(date)" ----"
if [ "$DIR_CREATED" == "yes" ]; then
	echo "Creata directory per l'anno $YEAR_DIR"
fi
python $CUSTOM_SCRIPTS_DIR/CategorieMensili.py
exit_code=$?
echo "---- Esecuzione terminata ----"
exit $exit_code
