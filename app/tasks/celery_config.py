"""Celery configuration"""
from celery import Celery
import os

def make_celery(app_name=__name__):
    """Create Celery instance"""
    broker = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    celery_app = Celery(
        app_name,
        broker=broker,
        backend=backend
    )
    
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,
        task_soft_time_limit=20 * 60,
    )
    
    return celery_app

celery = make_celery()
