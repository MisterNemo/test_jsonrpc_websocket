#!/bin/bash
set -e

exec gunicorn --chdir /code config.asgi:application --workers 2 --bind :8000  --worker-class uvicorn.workers.UvicornWorker

