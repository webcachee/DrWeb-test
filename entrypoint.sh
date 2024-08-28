#!/bin/sh
# entrypoint.sh

echo "Running migrations..."
flask db upgrade

echo "Starting Gunicorn..."
gunicorn -b 0.0.0.0:5000 run:app