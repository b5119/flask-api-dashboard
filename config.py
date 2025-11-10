import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_key_change_in_production")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///news_dashboard.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Keys
    NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")  # Changed to match news_api.py
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")  # Keep for backwards compatibility
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")  # For weather_api.py
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # Keep for backwards compatibility
    CRYPTO_API_KEY = os.getenv("CRYPTO_API_KEY")
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.db"

# Configuration dictionary - required by __init__.py
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}