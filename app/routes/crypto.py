"""
Cryptocurrency Routes
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import CryptoHolding
from app.api.crypto_api import CryptoAPI

crypto_bp = Blueprint('crypto', __name__)
crypto_api = CryptoAPI()


@crypto_bp.route('/')
def index():
    """Crypto home page"""
    return render_template('crypto.html',
                         title='Cryptocurrency',
                         active_page='crypto')


@crypto_bp.route('/api/prices')
def get_prices():
    """Get cryptocurrency prices"""
    coins = request.args.getlist('coins')
    if not coins:
        coins = ['bitcoin', 'ethereum', 'cardano', 'ripple', 'solana']
    
    vs_currency = request.args.get('vs_currency', 'usd')
    
    try:
        prices = crypto_api.get_prices(coins)
        
        return jsonify({
            'success': True,
            'prices': prices
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@crypto_bp.route('/api/coin/<coin_id>')
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


@crypto_bp.route('/api/trending')
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


@crypto_bp.route('/api/top')
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
