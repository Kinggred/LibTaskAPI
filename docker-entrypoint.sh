#!/bin/sh
set -e

alembic -c app/alembic.ini upgrade head

fastapi run app/api/main.py --host 0.0.0.0 --port 8000