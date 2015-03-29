#!/bin/bash
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
if [ ! -f $CURRENT_SCRIPT_DIR/Environment.sh ]; then
    echo "Custom scripts are not configured. Please run install.py"
    exit 1
fi
source $CURRENT_SCRIPT_DIR/Environment.sh
TEMP_LOG_FILE="/tmp/${1}ExecutionLog.log"
case "$1" in
	"lingue")
		$CUSTOM_SCRIPTS_DIR/EseguiLingue.sh &> $TEMP_LOG_FILE
		exit_status=$?
		;;
	"categorie")
		python $CUSTOM_SCRIPTS_DIR/CategorieMensili.py &> $TEMP_LOG_FILE
		exit_status=$?
		;;
	"portale")
		python $CUSTOM_SCRIPTS_DIR/Portale.py &> $TEMP_LOG_FILE
		exit_status=$?
		;;
	*)
		echo "Unknown command"
		exit 2
		;;
esac
python $CUSTOM_SCRIPTS_DIR/registerLog.py $1 $exit_status $TEMP_LOG_FILE