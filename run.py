"""
Flask API Dashboard - Main Application Entry Point
"""

from app import create_app, db
from app.models import User, SavedArticle, CryptoHolding
import os

# ✅ Fixed line — no config argument needed
app = create_app()

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

@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    # Add sample data here
    print("✅ Database seeded!")

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
