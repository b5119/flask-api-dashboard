"""
Main Routes - Dashboard and Home
"""

from flask import Blueprint, render_template, jsonify, request
from app.api.news_api import NewsAPI
from app.api.weather_api import WeatherAPI
from app.api.crypto_api import CryptoAPI
from app.api.github_api import GitHubAPI

main_bp = Blueprint('main', __name__)

# Initialize API clients
news_api = NewsAPI()
weather_api = WeatherAPI()
crypto_api = CryptoAPI()
github_api = GitHubAPI()


@main_bp.route('/')
def index():
    """Dashboard home page"""
    return render_template('index.html',
                         title='Dashboard',
                         active_page='dashboard')


@main_bp.route('/dashboard/data')
def dashboard_data():
    """Get all dashboard data via AJAX"""
    try:
        # Fetch data from all APIs
        news = news_api.get_top_headlines(category='technology', page_size=5)
        weather = weather_api.get_current_weather('London')
        crypto = crypto_api.get_prices(['bitcoin', 'ethereum', 'cardano'])
        github = github_api.get_trending_repos(limit=5)
        
        return jsonify({
            'success': True,
            'data': {
                'news': news,
                'weather': weather,
                'crypto': crypto,
                'github': github
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html',
                         title='About',
                         active_page='about')


@main_bp.route('/api/status')
def api_status():
    """Check API availability"""
    status = {
        'news': news_api.check_status(),
        'weather': weather_api.check_status(),
        'crypto': crypto_api.check_status(),
        'github': github_api.check_status()
    }
    
    return jsonify(status)


@main_bp.route('/search')
def search():
    """Global search across all services"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'No search query provided'
        }), 400
    
    results = {
        'news': news_api.search(query, page_size=10),
        'github': github_api.search_repositories(query, limit=10)
    }
    
    return jsonify({
        'success': True,
        'query': query,
        'results': results
    })


@main_bp.route('/settings')
def settings():
    """User settings page"""
    return render_template('settings.html',
                         title='Settings',
                         active_page='settings')