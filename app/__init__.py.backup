from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from app.routes.main import main_bp
    from app.routes.weather import weather_bp
    from app.routes.news import news_bp
    from app.routes.crypto import crypto_bp
    from app.routes.github import github_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(crypto_bp, url_prefix='/crypto')
    app.register_blueprint(github_bp, url_prefix='/github')

    return app