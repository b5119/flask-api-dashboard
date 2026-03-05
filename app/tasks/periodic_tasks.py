"""Periodic task scheduling"""
from app.tasks.celery_config import celery
from celery.schedules import crontab

# Configure periodic tasks
celery.conf.beat_schedule = {
    'check-price-alerts-every-5-minutes': {
        'task': 'tasks.check_all_price_alerts',
        'schedule': 300.0,  # Every 5 minutes
    },
    'cleanup-old-data-daily': {
        'task': 'tasks.cleanup_old_data',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'fetch-news-every-hour': {
        'task': 'tasks.fetch_news',
        'schedule': 3600.0,  # Every hour
    },
}
