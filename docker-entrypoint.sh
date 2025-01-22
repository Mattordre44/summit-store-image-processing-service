#!/bin/sh

echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') Starting the image processing service..."

# Execute the Python application
exec python src/app.py