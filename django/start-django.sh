#!/bin/bash
sleep 5
python manage.py makemigrations twitteranalytics
python manage.py migrate
python manage.py collectstatic --noinput
uwsgi --socket :8001 --module config.wsgi
# uwsgi --socket :8001 --module chatapp.wsgi & daphne -b 0.0.0.0 -p 3001 --ping-interval 10 --ping-timeout 120 chatapp.asgi:application
