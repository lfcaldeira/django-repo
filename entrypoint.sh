#!/bin/sh

python manage.py migrate --noinput
python init_admin.py

exec "$@"