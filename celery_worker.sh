#!/bin/bash
# Start Celery worker

source venv/bin/activate
celery -A app.tasks.celery_config:celery worker --loglevel=info
