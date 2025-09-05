#!/bin/sh
set -e

# Wait for db if necessary (not required for sqlite)
python manage.py migrate --noinput

# Run server if default command not provided
exec "$@"
