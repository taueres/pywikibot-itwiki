#!/bin/bash
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#Load environment variables
source $CURRENT_SCRIPT_DIR/Environment.sh
case "$1" in
	"lingue")
		$CUSTOM_SCRIPTS_DIR/EseguiLingue.sh >> $LOG_FILE_LINGUE 2>&1
		exit_status=$?
		;;
	"categorie")
		#Don't redirect output because we don't know whether the log directory exists
		$CUSTOM_SCRIPTS_DIR/EseguiCategorie.sh
		exit_status=$?
		;;
	"rotazione")
		python $CUSTOM_SCRIPTS_DIR/logRotation.py
		exit_status=$?
		;;
	"portale")
		python $CUSTOM_SCRIPTS_DIR/Portale.py &> $LOG_DIR_PORTALE/$(date +%Y%m%d).log
		exit_status=$?
		;;
	*)
		email_text="From: $SERVER_NAME <$SERVER_EMAIL>
To: Administrator <$ADMIN_EMAIL>
Subject: Error with cron job
Content-Type: text/plain

Wrong parameter when invoking \"Esegui.sh\" -> \"$1\" given.
Execution interrupted. Please check what went wrong."
		echo -e "$email_text" | sendmail $ADMIN_EMAIL
		exit 2
		;;
esac

if [ $exit_status != 0 ]; then
	email_text="From: $SERVER_NAME <$SERVER_EMAIL>
To: Administrator <$ADMIN_EMAIL>
Subject: Error when executing $1 job
Content-Type: text/plain

Exit status for the job $1 is $exit_status
Execution interrupted. Please check what went wrong."
	echo -e "$email_text" | sendmail $ADMIN_EMAIL
fi
