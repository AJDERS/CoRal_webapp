#!/usr/bin/env bash

echo "Installing CoRal WebApp!"

echo "Setting up ssh keys"
SSHDIR="~/.ssh/config"
cd ~/Desktop
if [ -d "$SSHDIR" ]; then
  cp -f ~/Desktop/config ~/.ssh/config
  cp -f ~/Desktop/id_ed25519 ~/.ssh/id_ed25519
  ssh-add ~/.ssh/id_ed25519
else
  touch ~/.ssh/config
  cp -f ~/Desktop/config ~/.ssh/config
  cp -f ~/Desktop/id_ed25519 ~/.ssh/id_ed25519
  ssh-add ~/.ssh/id_ed25519
fi

echo "Cloning CoRal Webapp"
DIR="CoRal_webapp"
if [ -d "$DIR" ]; then
  cd $DIR
  git stash
  git checkout master
  git pull

else
  git clone https://github.com/AJDERS/CoRal_webapp ~/Desktop/CoRal_webapp
  cd ~/Desktop/CoRal_webapp
  git pull origin master
fi

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

