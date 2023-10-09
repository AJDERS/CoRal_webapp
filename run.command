#!/usr/bin/env bash

echo "Openning CoRal WebApp!"

cd ~/Desktop/CoRal_webapp


DIR1=".venv"
if [ -d "$DIR1" ]; then
  git stash
  git checkout master
  git pull
  source .venv/bin/activate
  python3 manage.py migrate --run-syncdb
  open -a "Google Chrome" http://127.0.0.1:8000/
  python3 manage.py runserver

else
  git stash
  git checkout master
  git pull
  python3 -m venv .venv
  source .venv/bin/activate
  pip3 install -r requirements_collect.txt
  python3 manage.py migrate --run-syncdb
  open -a "Google Chrome" http://127.0.0.1:8000/
  python3 manage.py runserver
fi

