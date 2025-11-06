"""
Database Models
"""

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    saved_articles = db.relationship('SavedArticle', backref='user', lazy='dynamic')
    crypto_holdings = db.relationship('CryptoHolding', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
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
    source = db.Column(db.String(100))
    published_at = db.Column(db.DateTime)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    
    def __repr__(self):
        return f'<SavedArticle {self.title[:30]}>'


class CryptoHolding(db.Model):
    """Cryptocurrency portfolio holdings"""
    __tablename__ = 'crypto_holdings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)
    coin_name = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    purchase_price = db.Column(db.Float)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<CryptoHolding {self.coin_name}: {self.amount}>'


class WeatherLocation(db.Model):
    """Saved weather locations"""
    __tablename__ = 'weather_locations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(2))
    is_default = db.Column(db.Boolean, default=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('weather_locations', lazy='dynamic'))
    
    def __repr__(self):
        return f'<WeatherLocation {self.city}>'


class GitHubRepo(db.Model):
    """Saved GitHub repositories"""
    __tablename__ = 'github_repos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    stars = db.Column(db.Integer)
    forks = db.Column(db.Integer)
    language = db.Column(db.String(50))
    last_updated = db.Column(db.DateTime)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('github_repos', lazy='dynamic'))
    
    def __repr__(self):
        return f'<GitHubRepo {self.full_name}>'


class PriceAlert(db.Model):
    """Cryptocurrency price alerts"""
    __tablename__ = 'price_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    coin_id = db.Column(db.String(50), nullable=False)
    coin_name = db.Column(db.String(100))
    target_price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.String(10))
    is_active = db.Column(db.Boolean, default=True)
    triggered = db.Column(db.Boolean, default=False)
    triggered_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('price_alerts', lazy='dynamic'))
    
    def __repr__(self):
        return f'<PriceAlert {self.coin_name} {self.condition} ${self.target_price}>'


class NotificationLog(db.Model):
    """Log of sent notifications"""
    __tablename__ = 'notification_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(20))
    recipient = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    status = db.Column(db.String(20))
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    error_message = db.Column(db.Text)
    
    user = db.relationship('User', backref=db.backref('notification_logs', lazy='dynamic'))
    
    def __repr__(self):
        return f'<NotificationLog {self.notification_type} to {self.recipient}>'