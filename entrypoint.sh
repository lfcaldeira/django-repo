#!/bin/sh

python manage.py migrate --noinput
python manage.py makemigrations MapsBORA
python manage.py migrate MapsBORA
python init_admin.py

exec "$@"