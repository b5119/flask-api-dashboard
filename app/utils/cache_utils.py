"""Cache utility functions"""

def clear_cache(cache, pattern='*'):
    """Clear cache entries matching pattern"""
    from redis import Redis
    import os
    
    redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    r = Redis.from_url(redis_url)
    
    keys = r.keys(f'dashboard_{pattern}')
    if keys:
        r.delete(*keys)
    
    return len(keys)

def warm_cache(cache):
    """Pre-populate cache with frequently accessed data"""
    from app.api.news_api import NewsAPI
    from app.api.crypto_api import CryptoAPI
    
    # Cache news
    news_api = NewsAPI()
    cache.set('news_headlines', news_api.get_top_headlines(), timeout=600)
    
    # Cache crypto prices
    crypto_api = CryptoAPI()
    cache.set('crypto_prices', crypto_api.get_prices(['bitcoin', 'ethereum']), timeout=60)
