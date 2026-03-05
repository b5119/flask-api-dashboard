"""Database optimization utilities"""
from flask_sqlalchemy import SQLAlchemy

def optimize_queries(db):
    """Add indexes to frequently queried columns"""
    from sqlalchemy import Index
    from app.models import User, CryptoHolding, SavedArticle, PriceAlert
    
    # Add indexes
    indexes = [
        Index('idx_user_email', User.email),
        Index('idx_crypto_user_coin', CryptoHolding.user_id, CryptoHolding.coin_id),
        Index('idx_article_user', SavedArticle.user_id),
        Index('idx_alert_user_active', PriceAlert.user_id, PriceAlert.active),
    ]
    
    for index in indexes:
        if not index.exists(db.engine):
            index.create(db.engine)

def analyze_slow_queries(db):
    """Analyze slow database queries"""
    from flask import current_app
    import logging
    
    # Enable query logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    current_app.config['SQLALCHEMY_ECHO'] = True
    current_app.config['SQLALCHEMY_RECORD_QUERIES'] = True

def vacuum_database():
    """Optimize SQLite database (development only)"""
    from app import db
    db.session.execute('VACUUM')
    db.session.commit()
