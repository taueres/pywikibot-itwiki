#!/bin/bash
# Setta le variabili d'ambiente necessarie per eseguire gli script manualmente 
# Modo d'utilizzo: ./EseguiManuale.sh ./EseguiLingue.sh
# Oppure: ./EseguiManuale.sh "python /home/sergio/pywikibot/core/pwb.py login.py"
# Questo file è stato ideato per essere eseguire i comandi interni di pywikibot
# come ad esempio il file login.py
# Gli script di custom possono essere eseguiti in un ambiente più realistico
# con ./Esegui.sh categorie oppure ./Esegui.sh lingue
# In questo modo l'output viene ridirezionato verso i file di log
#
# In sintesi:
# ./EseguiManuale.sh ./EseguiLingue.sh -> output a video
# ./Esegui.sh lingue -> output nei file di log (come in CRON)

source Environment.sh
export MANUAL_MODE="yes"
echo "Variabili d'ambiente settate"
echo "Eseguo il comando specificato: $1"
exec $1
