#!/bin/sh

set -e

python kyrios/manage.py wait_for_db
python kyrios/manage.py collectstatic --noinput
python kyrios/manage.py migrate

cd kyrios
uwsgi --socket :8000 --workers 4 --master --enable-threads --module kyrios.wsgi:application --env DJANGO_SETTINGS_MODULE=kyrios.settings.production