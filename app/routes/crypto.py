"""
Cryptocurrency Routes
"""

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import CryptoHolding, PriceAlert
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


@crypto_bp.route('/api/chart/<coin_id>')
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


@crypto_bp.route('/portfolio')
@login_required
def portfolio():
    """User's crypto portfolio"""
    holdings = current_user.crypto_holdings.all()
    
    return render_template('crypto_portfolio.html',
                         title='My Portfolio',
                         active_page='crypto',
                         holdings=holdings)


@crypto_bp.route('/portfolio/add', methods=['POST'])
@login_required
def add_holding():
    """Add crypto holding to portfolio"""
    data = request.get_json()
    
    coin_id = data.get('coin_id')
    coin_name = data.get('coin_name')
    amount = data.get('amount')
    purchase_price = data.get('purchase_price')
    
    if not all([coin_id, amount]):
        return jsonify({
            'success': False,
            'error': 'Missing required fields'
        }), 400
    
    try:
        holding = CryptoHolding(
            user_id=current_user.id,
            coin_id=coin_id,
            coin_name=coin_name,
            amount=float(amount),
            purchase_price=float(purchase_price) if purchase_price else None
        )
        
        db.session.add(holding)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Holding added successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@crypto_bp.route('/portfolio/delete/<int:holding_id>', methods=['DELETE'])
@login_required
def delete_holding(holding_id):
    """Delete crypto holding"""
    holding = CryptoHolding.query.get_or_404(holding_id)
    
    if holding.user_id != current_user.id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized'
        }), 403
    
    try:
        db.session.delete(holding)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Holding deleted successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500