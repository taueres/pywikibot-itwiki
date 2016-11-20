#!/bin/bash
CURRENT_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "TauerBot is running..."

if [ -z "${PYWIKIBOT2_DIR}" ]; then
    echo "Please configure environment variables properly!"
    exit 1
fi

if [ -z "${1}" ]; then
    echo "At least one argument is required. Possible choices are: language-counters, monthly-categories, portale-template."
    exit 1
fi

TEMP_LOG_FILE="/tmp/${1}ExecutionLog.log"

python ${CURRENT_SCRIPT_DIR}/run.py ${1} &> ${TEMP_LOG_FILE}
exit_status=$?

python ${CURRENT_SCRIPT_DIR}/register_log.py ${1} ${exit_status} ${TEMP_LOG_FILE}
exit $?
