#!/usr/bin/env bash

echo "Cleaning the webapp means that all audio recordings and metadata will be permanently deleted. You should make sure you have backed up any audio recordings you want to keep. If you are sure you want to clean the webapp, type 'y' and press enter. Otherwise, type 'n' and press enter."
echo "Are you sure you want to clean the CoRal Webapp? (y/n)"
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
    echo "Cleaning the CoRal Webapp!"
else
    echo "Exiting the CoRal Webapp!"
    exit 1
fi

shopt -s extglob
cd ~/Desktop/CoRal_webapp/audio_files
rm -v !("processed_articles.csv")
cd ~/Desktop/CoRal_webapp
rm db.sqlite3

echo "The webapp is now clean!"
echo "Running the CoRal WebApp!"
DIR1=".venv"
if [ -d "$DIR1" ]; then
  source .venv/bin/activate
  python3 manage.py migrate --run-syncdb
  open -a "Google Chrome" http://127.0.0.1:8000/
  python3 manage.py runserver

else
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install -r requirements_collect.txt
  python3 manage.py migrate --run-syncdb
  open -a "Google Chrome" http://127.0.0.1:8000/
  python3 manage.py runserver
fi