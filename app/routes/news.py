"""
News Routes
Handles news-related endpoints
"""

from flask import Blueprint, jsonify, request
from app.api.news_api import NewsAPI

news_bp = Blueprint('news', __name__)
news_api = NewsAPI()

@news_bp.route('/headlines', methods=['GET'])
def get_headlines():
    """Get top headlines"""
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
    
    return jsonify(result)

@news_bp.route('/search', methods=['GET'])
def search_news():
    """Search news articles"""
    query = request.args.get('q')
    
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
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
    
    return jsonify(result)

@news_bp.route('/sources', methods=['GET'])
def get_sources():
    """Get available news sources"""
    category = request.args.get('category')
    language = request.args.get('language', 'en')
    country = request.args.get('country')
    
    sources = news_api.get_sources(
        category=category,
        language=language,
        country=country
    )
    
    return jsonify({'sources': sources})

@news_bp.route('/status', methods=['GET'])
def check_status():
    """Check if News API is configured"""
    is_configured = news_api.check_status()
    
    return jsonify({
        'configured': is_configured,
        'message': 'News API is configured' if is_configured else 'News API key not found'
    })

@news_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available news categories"""
    categories = [
        'business',
        'entertainment',
        'general',
        'health',
        'science',
        'sports',
        'technology'
    ]
    
    return jsonify({'categories': categories})