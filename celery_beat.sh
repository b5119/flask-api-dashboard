#!/bin/bash
# Start Celery beat scheduler

source venv/bin/activate
celery -A app.tasks.celery_config:celery beat --loglevel=info
