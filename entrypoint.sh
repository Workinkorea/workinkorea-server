#!/bin/sh
set -e

# database migration
# uv run alembic upgrade head

# start server
uv run uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"