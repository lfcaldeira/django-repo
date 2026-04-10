#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python init_admin.py

exec "$@"