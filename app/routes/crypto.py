"""
Cryptocurrency Routes
Handles crypto-related endpoints (API-only, no authentication)
"""

from flask import Blueprint, jsonify, request
from app.api.crypto_api import CryptoAPI

crypto_bp = Blueprint('crypto', __name__)
crypto_api = CryptoAPI()

@crypto_bp.route('/prices')
def get_prices():
    """Get cryptocurrency prices"""
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

@crypto_bp.route('/coin/<coin_id>')
def get_coin_details(coin_id):
    """Get detailed coin information"""
    try:
        details = crypto_api.get_coin_details(coin_id)
        
        if details:
            return jsonify({
                'success': True,
                'coin': details
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Coin not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@crypto_bp.route('/trending')
def get_trending():
    """Get trending cryptocurrencies"""
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

@crypto_bp.route('/top')
def get_top_coins():
    """Get top cryptocurrencies by market cap"""
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

@crypto_bp.route('/chart/<coin_id>')
def get_chart_data(coin_id):
    """Get historical chart data"""
    vs_currency = request.args.get('vs_currency', 'usd')
    days = request.args.get('days', 7, type=int)
    
    try:
        chart_data = crypto_api.get_market_chart(coin_id, vs_currency, days)
        
        return jsonify({
            'success': True,
            'chart_data': chart_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@crypto_bp.route('/status')
def check_status():
    """Check if Crypto API is configured and available"""
    is_configured = crypto_api.check_status()
    
    return jsonify({
        'configured': is_configured,
        'message': 'Crypto API is available' if is_configured else 'Crypto API unavailable'
    })