"""Cache configuration"""
from flask_caching import Cache
import os

def init_cache(app):
    """Initialize Flask-Caching"""
    cache_config = {
        'CACHE_TYPE': 'redis',
        'CACHE_REDIS_URL': os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
        'CACHE_DEFAULT_TIMEOUT': 300,
        'CACHE_KEY_PREFIX': 'dashboard_'
    }
    
    cache = Cache()
    cache.init_app(app, config=cache_config)
    
    return cache
