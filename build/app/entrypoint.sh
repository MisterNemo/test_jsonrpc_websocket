#!/bin/bash
set -e

#exec gunicorn --chdir /code config.wsgi --log-level debug --access-logfile /logs/gunicorn-access.log --error-logfile /logs/gunicorn-error.log -b 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000

exec gunicorn --chdir /code config.asgi:application --workers 2 --bind :8000  --worker-class uvicorn.workers.UvicornWorker

