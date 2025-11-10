"""
Database Models
Defines all database models for the application
"""

from app import db
from datetime import datetime

class User(db.Model):
    """User model"""
    __tablename__ = 'user'  # Changed to match your ForeignKey references
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    saved_articles = db.relationship('SavedArticle', backref='user', lazy=True, cascade='all, delete-orphan')
    crypto_holdings = db.relationship('CryptoHolding', backref='user', lazy=True, cascade='all, delete-orphan')
    price_alerts = db.relationship('PriceAlert', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class SavedArticle(db.Model):
    """Saved news articles"""
    __tablename__ = 'saved_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(500))
    source = db.Column(db.String(100))
    published_at = db.Column(db.String(50))
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<SavedArticle {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'image_url': self.image_url,
            'source': self.source,
            'published_at': self.published_at,
            'saved_at': self.saved_at.isoformat()
        }

class CryptoHolding(db.Model):
    """Cryptocurrency holdings/portfolio"""
    __tablename__ = 'crypto_holdings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)  # e.g., 'bitcoin'
    coin_symbol = db.Column(db.String(10), nullable=False)  # e.g., 'BTC'
    coin_name = db.Column(db.String(100), nullable=False)  # e.g., 'Bitcoin'
    amount = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float)  # Price when purchased
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CryptoHolding {self.coin_symbol}: {self.amount}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'coin_id': self.coin_id,
            'coin_symbol': self.coin_symbol,
            'coin_name': self.coin_name,
            'amount': self.amount,
            'purchase_price': self.purchase_price,
            'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class PriceAlert(db.Model):
    """Cryptocurrency price alerts"""
    __tablename__ = 'price_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)
    coin_symbol = db.Column(db.String(10), nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(10), nullable=False)  # 'above' or 'below'
    is_active = db.Column(db.Boolean, default=True)
    triggered = db.Column(db.Boolean, default=False)
    triggered_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PriceAlert {self.coin_symbol} {self.condition} ${self.target_price}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'coin_id': self.coin_id,
            'coin_symbol': self.coin_symbol,
            'target_price': self.target_price,
            'condition': self.condition,
            'is_active': self.is_active,
            'triggered': self.triggered,
            'triggered_at': self.triggered_at.isoformat() if self.triggered_at else None,
            'created_at': self.created_at.isoformat()
        }

class WeatherFavorite(db.Model):
    """Favorite weather locations"""
    __tablename__ = 'weather_favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='weather_favorites')
    
    def __repr__(self):
        return f'<WeatherFavorite {self.city}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'city': self.city,
            'country': self.country,
            'created_at': self.created_at.isoformat()
        }

class GitHubRepo(db.Model):
    """Starred/saved GitHub repositories"""
    __tablename__ = 'github_repos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    repo_id = db.Column(db.Integer, nullable=False)  # GitHub repo ID
    repo_name = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    html_url = db.Column(db.String(500), nullable=False)
    language = db.Column(db.String(50))
    stars = db.Column(db.Integer, default=0)
    forks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='github_repos')
    
    def __repr__(self):
        return f'<GitHubRepo {self.full_name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'repo_id': self.repo_id,
            'repo_name': self.repo_name,
            'full_name': self.full_name,
            'description': self.description,
            'html_url': self.html_url,
            'language': self.language,
            'stars': self.stars,
            'forks': self.forks,
            'created_at': self.created_at.isoformat()
        }