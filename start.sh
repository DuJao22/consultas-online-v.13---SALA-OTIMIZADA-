#!/bin/bash

echo "Iniciando MedConnect..."

python3 -c "from app import init_db; init_db()"

PORT=${PORT:-5000}

exec gunicorn -c gunicorn_config.py app:app
