#!/bin/bash
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "$PYWIKIBOT2_DIR" ]; then
    echo "Please configure environment variables properly!"
    exit 1
fi

TEMP_LOG_FILE="/tmp/${1}ExecutionLog.log"
case "$1" in
    "lingue")
        ${CURRENT_SCRIPT_DIR}/src/EseguiLingue.sh &> ${TEMP_LOG_FILE}
        exit_status=$?
        ;;
    "categorie")
        python ${CURRENT_SCRIPT_DIR}/src/CategorieMensili.py &> ${TEMP_LOG_FILE}
        exit_status=$?
        ;;
    "portale")
        python ${CURRENT_SCRIPT_DIR}/src/Portale.py ${2} &> ${TEMP_LOG_FILE}
        exit_status=$?
        ;;
    *)
        echo "Esegui.sh - ERROR: provided '$1' command is not recognized"
        exit 2
        ;;
esac
python ${CURRENT_SCRIPT_DIR}/src/registerLog.py $1 ${exit_status} ${TEMP_LOG_FILE}
