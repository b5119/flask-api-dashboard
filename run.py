"""
Flask Application Entry Point with WebSocket Support
"""
from app import create_app, db
from app.models import User, SavedArticle, CryptoHolding
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'SavedArticle': SavedArticle,
        'CryptoHolding': CryptoHolding
    }

@app.cli.command()
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print("✅ Database initialized!")

if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
