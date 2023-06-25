#!/bin/bash

# start gunicorn
# Ключ -d нужен, чтобы процесс не блокировал терминал. Он запускает gunicorn как демона.
# Иначе следующая команда выполнится только когда gunicorn завершится.
gunicorn app.main:app -D --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

docker compose up
