#!/usr/bin/env bash

git pull
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
sudo cp -vr game_runner /opt/uiai2018/
