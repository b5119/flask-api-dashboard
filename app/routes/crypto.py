"""
Crypto Routes
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

@crypto_bp.route('/home')
def crypto_home():
    """Alias for crypto home (required by templates)"""
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
        return jsonify({'success': True, 'prices': prices})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crypto_bp.route('/api/coin/<coin_id>')
def api_coin_details(coin_id):
    """API endpoint for coin details"""
    try:
        details = crypto_api.get_coin_details(coin_id)
        if details:
            return jsonify({'success': True, 'coin': details})
        else:
            return jsonify({'success': False, 'error': 'Coin not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crypto_bp.route('/api/trending')
def api_trending():
    """API endpoint for trending coins"""
    try:
        trending = crypto_api.get_trending()
        return jsonify({'success': True, 'trending': trending})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crypto_bp.route('/api/top')
def api_top():
    """API endpoint for top coins"""
    vs_currency = request.args.get('vs_currency', 'usd')
    limit = request.args.get('limit', 100, type=int)
    page = request.args.get('page', 1, type=int)
    
    try:
        coins = crypto_api.get_top_coins(vs_currency, limit, page)
        return jsonify({'success': True, 'coins': coins})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crypto_bp.route('/api/chart/<coin_id>')
def api_chart(coin_id):
    """API endpoint for chart data"""
    vs_currency = request.args.get('vs_currency', 'usd')
    days = request.args.get('days', 7, type=int)
    
    try:
        chart_data = crypto_api.get_market_chart(coin_id, vs_currency, days)
        return jsonify({'success': True, 'chart_data': chart_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500