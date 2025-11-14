"""
News Routes
"""
from flask import Blueprint, render_template, jsonify, request
from app.api.news_api import NewsAPI

news_bp = Blueprint('news', __name__)
news_api = NewsAPI()

@news_bp.route('/')
def index():
    """News home page"""
    return render_template('news.html',
                         title='News',
                         active_page='news',
                         category='technology',
                         country='us')

@news_bp.route('/home')
def news_home():
    """Alias for news home (required by templates)"""
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

@news_bp.route('/api/search')
def search_news():
    """Search news articles"""
    query = request.args.get('q')
    if not query:
        return jsonify({'success': False, 'error': 'Query required'}), 400
    
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    language = request.args.get('language', 'en')
    sort_by = request.args.get('sort_by', 'publishedAt')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 20))
    
    result = news_api.search_everything(
        query=query,
        from_date=from_date,
        to_date=to_date,
        language=language,
        sort_by=sort_by,
        page=page,
        page_size=page_size
    )
    
    return jsonify({
        'success': True,
        'articles': result.get('articles', []),
        'total_results': result.get('totalResults', 0)
    })

@news_bp.route('/api/sources')
def get_sources():
    """Get available news sources"""
    category = request.args.get('category')
    language = request.args.get('language', 'en')
    country = request.args.get('country')
    
    sources = news_api.get_sources(category=category, language=language, country=country)
    return jsonify({'success': True, 'sources': sources})

@news_bp.route('/api/categories')
def get_categories():
    """Get available news categories"""
    categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    return jsonify({'success': True, 'categories': categories})