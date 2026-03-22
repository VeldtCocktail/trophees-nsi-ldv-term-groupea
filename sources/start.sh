#!/bin/bash

# on récupère le répertoire où se trouve ce script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# on remonte d'un niveau pour obtenir la racine du projet
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# on se place à la racine du projet pour que les chemins relatifs fonctionnent
cd "$PROJECT_ROOT" || exit 1

# on vérifie si l'option --debug a été passée en argument
DEBUG=0
for arg in "$@"; do
    if [ "$arg" = "--debug" ]; then
        DEBUG=1
    fi
done

# on utilise l'interpréteur Python du virtualenv s'il existe, sinon celui
# du système
VENV_PATH="./.venv/bin/python3"
PYTHON_CMD="python3"
if [ -f "$VENV_PATH" ]; then
    PYTHON_CMD="$VENV_PATH"
fi

# on lance l'application Python avec les variables d'environnement nécessaires
# à QtWebEngine, en passant l'option --debug à main.py si elle a été demandée
QT_QPA_PLATFORM=xcb \
QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox" \
QT_DEBUG_PLUGINS=1 \
$PYTHON_CMD sources/main.py $([ $DEBUG -eq 1 ] && echo "--debug")