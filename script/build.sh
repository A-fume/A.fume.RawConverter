#!/bin/bash

BASEDIR=$(dirname "$0")
echo "$BASEDIR"

mkdir "${BASEDIR}/../out" || :
cd "${BASEDIR}/../out" || exit
pyinstaller --onefile -n A_fume_Excel_Converter --paths "../venv/lib/python3.7/site-packages" --clean ../run.py
cp ../.env ./dist/.env
cp ../script/run.sh ./dist/run.sh
