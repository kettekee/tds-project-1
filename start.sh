#!/bin/bash
set -e

echo "Downloading the latest datagen.py..."
curl -o datagen.py https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py
echo "datagen.py updated successfully."

echo "Starting FastAPI server..."
exec uvicorn app:app --host 0.0.0.0 --port 8000