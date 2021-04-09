#!/bin/bash

python manage.py migrate

if [ "$APP_ENV" = "development" ]; then
  FLASK_ENV=development flask run --host=0.0.0.0
elif [ "$APP_ENV" = "celery" ]; then
  celery -A tasks worker -l debug -f ./celery.log
else
  uwsgi --http 0.0.0.0:5000 --module app:app --enable-threads
fi
