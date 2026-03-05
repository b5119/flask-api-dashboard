"""Background task definitions"""
from app.tasks.celery_config import celery
from datetime import datetime

@celery.task(name='tasks.fetch_news')
def fetch_news_async():
    """Fetch news in background"""
    from app.api.news_api import NewsAPI
    news_api = NewsAPI()
    headlines = news_api.get_top_headlines(page_size=20)
    return headlines

@celery.task(name='tasks.fetch_crypto_prices')
def fetch_crypto_prices_async(coin_ids):
    """Fetch crypto prices in background"""
    from app.api.crypto_api import CryptoAPI
    crypto_api = CryptoAPI()
    prices = crypto_api.get_prices(coin_ids)
    return prices

@celery.task(name='tasks.send_price_alert')
def send_price_alert(email, coin, price, condition):
    """Send price alert email"""
    from app.api.notification_api import NotificationAPI
    notifier = NotificationAPI()
    
    subject = f"🚨 Price Alert: {coin.upper()}"
    message = f"{coin.upper()} has {condition} ${price:,.2f}"
    
    result = notifier.send_email(
        to_email=email,
        subject=subject,
        content=message
    )
    
    return result

@celery.task(name='tasks.check_all_price_alerts')
def check_all_price_alerts():
    """Check all user price alerts"""
    from app.models import PriceAlert
    from app.api.crypto_api import CryptoAPI
    
    crypto_api = CryptoAPI()
    alerts = PriceAlert.query.filter_by(active=True).all()
    
    # Group alerts by coin
    coins = list(set([alert.coin_id for alert in alerts]))
    prices = crypto_api.get_prices(coins)
    
    triggered = []
    for alert in alerts:
        current_price = prices.get(alert.coin_id, {}).get('usd')
        
        if current_price:
            if alert.condition == 'above' and current_price >= alert.target_price:
                send_price_alert.delay(alert.user.email, alert.coin_id, current_price, 'reached')
                triggered.append(alert.id)
            elif alert.condition == 'below' and current_price <= alert.target_price:
                send_price_alert.delay(alert.user.email, alert.coin_id, current_price, 'dropped to')
                triggered.append(alert.id)
    
    return {'checked': len(alerts), 'triggered': len(triggered)}

@celery.task(name='tasks.cleanup_old_data')
def cleanup_old_data():
    """Clean up old data from database"""
    from app import db
    from app.models import UserActivity
    from datetime import timedelta
    
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    deleted = UserActivity.query.filter(UserActivity.timestamp < cutoff_date).delete()
    db.session.commit()
    
    return {'deleted': deleted}
