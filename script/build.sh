#!/bin/bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

cd "${BASEDIR}/../out" || exit
pyinstaller --onefile -n A_fume_Excel_Converter --paths "${BASEDIR}/../venv/lib/python3.7/site-packages" --clean ../run.py