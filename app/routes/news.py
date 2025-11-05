"""
News Routes
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from app.api.news_api import NewsAPI

news_bp = Blueprint('news', __name__)
news_api = NewsAPI()


@news_bp.route('/')
def index():
    """News home page"""
    category = request.args.get('category', 'general')
    country = request.args.get('country', 'us')
    
    return render_template('news.html',
                         title='News',
                         active_page='news',
                         category=category,
                         country=country)


@news_bp.route('/api/headlines')
def get_headlines():
    """Get top headlines via AJAX"""
    category = request.args.get('category', 'general')
    country = request.args.get('country', 'us')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    
    try:
        articles = news_api.get_top_headlines(
            category=category,
            country=country,
            page=page,
            page_size=page_size
        )
        
        return jsonify({
            'success': True,
            'articles': articles.get('articles', []),
            'total_results': articles.get('totalResults', 0)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/api/search')
def search_news():
    """Search news articles"""
    query = request.args.get('q', '')
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    language = request.args.get('language', 'en')
    sort_by = request.args.get('sort_by', 'publishedAt')
    page = request.args.get('page', 1, type=int)
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query required'
        }), 400
    
    try:
        results = news_api.search_everything(
            query=query,
            from_date=from_date,
            to_date=to_date,
            language=language,
            sort_by=sort_by,
            page=page
        )
        
        return jsonify({
            'success': True,
            'articles': results.get('articles', []),
            'total_results': results.get('totalResults', 0)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/api/sources')
def get_sources():
    """Get available news sources"""
    category = request.args.get('category')
    language = request.args.get('language', 'en')
    country = request.args.get('country')
    
    try:
        sources = news_api.get_sources(
            category=category,
            language=language,
            country=country
        )
        
        return jsonify({
            'success': True,
            'sources': sources
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@news_bp.route('/search')
def search_page():
    """News search page"""
    query = request.args.get('q', '')
    
    return render_template('news_search.html',
                         title=f'Search: {query}',
                         active_page='news',
                         query=query)