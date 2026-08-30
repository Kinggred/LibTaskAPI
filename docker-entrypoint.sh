#!/bin/sh
set -e

echo "Running database migrations..."
alembic -c app/alembic.ini upgrade head

if [ "${LOAD_FIXTURES:-false}" = "true" ]; then
    echo "Loading demo data..."
    python -m app.fixtures.load
fi

echo "Starting application..."
fastapi run app/api/main.py --host 0.0.0.0 --port 8000
