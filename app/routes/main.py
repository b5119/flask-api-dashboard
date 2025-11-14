"""
app/routes/main.py - Main routes with template rendering
"""
from flask import Blueprint, render_template, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Dashboard home page"""
    return render_template('index.html', 
                         title='Dashboard',
                         active_page='dashboard')

@main_bp.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    })

@main_bp.route('/dashboard/data')
def dashboard_data():
    """API endpoint for dashboard data"""
    from app.api.news_api import NewsAPI
    from app.api.weather_api import WeatherAPI
    from app.api.crypto_api import CryptoAPI
    from app.api.github_api import GitHubAPI
    
    news_api = NewsAPI()
    weather_api = WeatherAPI()
    crypto_api = CryptoAPI()
    github_api = GitHubAPI()
    
    try:
        # Get news
        news_data = news_api.get_top_headlines(page_size=5)
        
        # Get weather
        weather_data = weather_api.get_current_weather('London')
        
        # Get crypto
        crypto_data = crypto_api.get_prices(['bitcoin', 'ethereum', 'cardano'])
        
        # Get GitHub
        github_data = github_api.get_trending_repos(limit=5)
        
        return jsonify({
            'success': True,
            'data': {
                'news': news_data,
                'weather': weather_data,
                'crypto': crypto_data,
                'github': github_data
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


"""
app/routes/news.py - News routes with templates
"""
from flask import Blueprint, render_template, jsonify, request
from app.api.news_api import NewsAPI

news_bp = Blueprint('news', __name__)
news_api = NewsAPI()

@news_bp.route('/')
def index():
    """News home page - THIS IS THE ROUTE YOUR TEMPLATE NEEDS"""
    return render_template('news.html',
                         title='News',
                         active_page='news',
                         category='technology',
                         country='us')

# Also add alias for news_home
@news_bp.route('/home')
def news_home():
    """Alias for news home"""
    return index()

@news_bp.route('/api/headlines')
def api_headlines():
    """API endpoint for headlines"""
    country = request.args.get('country', 'us')
    category = request.args.get('category')
    query = request.args.get('q')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    result = news_api.get_top_headlines(
        country=country,
        category=category,
        query=query,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'success': True,
        'articles': result.get('articles', []),
        'total_results': result.get('totalResults', 0)
    })


"""
app/routes/weather.py - Weather routes with templates
"""
from flask import Blueprint, render_template, jsonify, request
from app.api.weather_api import WeatherAPI

weather_bp = Blueprint('weather', __name__)
weather_api = WeatherAPI()

@weather_bp.route('/')
def index():
    """Weather home page"""
    return render_template('weather.html',
                         title='Weather',
                         active_page='weather',
                         city='London')

# Alias for weather_home
@weather_bp.route('/home')
def weather_home():
    """Alias for weather home"""
    return index()

@weather_bp.route('/api/current/<city>')
def api_current(city):
    """API endpoint for current weather"""
    units = request.args.get('units', 'metric')
    result = weather_api.get_current_weather(city, units=units)
    
    if result:
        return jsonify({
            'success': True,
            'weather': result
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch weather data'
        }), 400

@weather_bp.route('/api/forecast/<city>')
def api_forecast(city):
    """API endpoint for weather forecast"""
    days = int(request.args.get('days', 5))
    units = request.args.get('units', 'metric')
    result = weather_api.get_forecast(city, days=days, units=units)
    
    if result:
        return jsonify({
            'success': True,
            'forecast': result
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Failed to fetch forecast data'
        }), 400


"""
app/routes/crypto.py - Crypto routes with templates
"""
from flask import Blueprint, render_template, jsonify, request
from app.api.crypto_api import CryptoAPI

crypto_bp = Blueprint('crypto', __name__)
crypto_api = CryptoAPI()

@crypto_bp.route('/')
def index():
    """Crypto home page"""
    return render_template('crypto.html',
                         title='Cryptocurrency',
                         active_page='crypto')

# Alias for crypto_home
@crypto_bp.route('/home')
def crypto_home():
    """Alias for crypto home"""
    return index()

@crypto_bp.route('/api/prices')
def api_prices():
    """API endpoint for crypto prices"""
    coins = request.args.getlist('coins')
    if not coins:
        coins = ['bitcoin', 'ethereum', 'cardano', 'ripple', 'solana']
    
    vs_currency = request.args.get('vs_currency', 'usd')
    
    try:
        prices = crypto_api.get_prices(coins, vs_currency)
        return jsonify({
            'success': True,
            'prices': prices
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@crypto_bp.route('/api/trending')
def api_trending():
    """API endpoint for trending coins"""
    try:
        trending = crypto_api.get_trending()
        return jsonify({
            'success': True,
            'trending': trending
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@crypto_bp.route('/api/top')
def api_top():
    """API endpoint for top coins"""
    vs_currency = request.args.get('vs_currency', 'usd')
    limit = request.args.get('limit', 100, type=int)
    page = request.args.get('page', 1, type=int)
    
    try:
        coins = crypto_api.get_top_coins(vs_currency, limit, page)
        return jsonify({
            'success': True,
            'coins': coins
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


"""
app/routes/github.py - GitHub routes with templates
"""
from flask import Blueprint, render_template, jsonify, request
from app.api.github_api import GitHubAPI

github_bp = Blueprint('github', __name__)
github_api = GitHubAPI()

@github_bp.route('/')
def index():
    """GitHub home page"""
    return render_template('github.html',
                         title='GitHub Explorer',
                         active_page='github')

# Alias for github_home
@github_bp.route('/home')
def github_home():
    """Alias for github home"""
    return index()

@github_bp.route('/api/trending')
def api_trending():
    """API endpoint for trending repos"""
    language = request.args.get('language')
    since = request.args.get('since', 'daily')
    limit = request.args.get('limit', 30, type=int)
    
    try:
        repos = github_api.get_trending_repos(language, since, limit)
        return jsonify({
            'success': True,
            'repositories': repos
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/api/search/repositories')
def api_search():
    """API endpoint for searching repos"""
    query = request.args.get('q')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter "q" is required'
        }), 400
    
    try:
        repos = github_api.search_repositories(query)
        return jsonify({
            'success': True,
            'results': repos
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/api/repo/<owner>/<repo>')
def api_repo(owner, repo):
    """API endpoint for repo details"""
    try:
        result = github_api.get_repository(owner, repo)
        if result:
            return jsonify({
                'success': True,
                'repository': result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Repository not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


"""
app/routes/notifications.py - Notifications routes with templates
"""
from flask import Blueprint, render_template, jsonify, request
from datetime import datetime

notifications_bp = Blueprint('notifications', __name__)

# In-memory storage
notifications_store = []
notification_id_counter = 1

@notifications_bp.route('/')
def index():
    """Notifications home page"""
    return render_template('notifications.html',
                         title='Notifications',
                         active_page='notifications')

@notifications_bp.route('/api/', methods=['GET'])
def api_get_all():
    """API endpoint to get all notifications"""
    return jsonify({
        'success': True,
        'notifications': notifications_store,
        'count': len(notifications_store)
    })

@notifications_bp.route('/api/', methods=['POST'])
def api_create():
    """API endpoint to create notification"""
    global notification_id_counter
    
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            'success': False,
            'error': 'Message is required'
        }), 400
    
    notification = {
        'id': notification_id_counter,
        'message': data['message'],
        'type': data.get('type', 'info'),
        'read': False,
        'created_at': datetime.utcnow().isoformat()
    }
    
    notifications_store.append(notification)
    notification_id_counter += 1
    
    return jsonify({
        'success': True,
        'notification': notification
    }), 201
@main_bp.route('/test-apis')
def test_apis():
    """Test if all APIs are responding"""
    from app.api.news_api import NewsAPI
    from app.api.weather_api import WeatherAPI
    from app.api.crypto_api import CryptoAPI
    from app.api.github_api import GitHubAPI
    
    results = {}
    
    # Test News API
    try:
        news_api = NewsAPI()
        results['news'] = 'OK' if news_api.check_status() else 'API Key Missing'
    except Exception as e:
        results['news'] = f'Error: {str(e)}'
    
    # Test Weather API
    try:
        weather_api = WeatherAPI()
        results['weather'] = 'OK' if weather_api.check_status() else 'API Key Missing'
    except Exception as e:
        results['weather'] = f'Error: {str(e)}'
    
    # Test Crypto API
    try:
        crypto_api = CryptoAPI()
        results['crypto'] = 'OK' if crypto_api.check_status() else 'Error'
    except Exception as e:
        results['crypto'] = f'Error: {str(e)}'
    
    # Test GitHub API
    try:
        github_api = GitHubAPI()
        results['github'] = 'OK' if github_api.check_status() else 'Error'
    except Exception as e:
        results['github'] = f'Error: {str(e)}'
    
    return jsonify(results)