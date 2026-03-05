"""Examples of cached routes"""
from flask import Blueprint
from app.utils.cache import cache

cached_bp = Blueprint('cached', __name__)

# Cache for 5 minutes
@cached_bp.route('/api/data')
@cache.cached(timeout=300)
def get_cached_data():
    # Expensive operation here
    pass

# Cache with dynamic key based on arguments
@cached_bp.route('/api/weather/<city>')
@cache.cached(timeout=600, key_prefix='weather_%s')
def get_weather(city):
    # Fetch weather data
    pass

# Cache with custom key function
def make_cache_key(*args, **kwargs):
    from flask import request
    return f"user_{request.args.get('user_id')}_data"

@cached_bp.route('/api/user/data')
@cache.cached(timeout=300, make_cache_key=make_cache_key)
def get_user_data():
    # User-specific data
    pass
