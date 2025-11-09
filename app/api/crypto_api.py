#!/usr/bin/env python3
"""
CryptoTracker Flask API
API wrapper for cryptocurrency tracking and portfolio management
"""
from flask import jsonify, request
from app.api.tracker import CryptoTracker

class CryptoAPI:
    """Crypto API handler class"""
    
    def __init__(self):
        self.tracker = CryptoTracker()
    
    def check_status(self):
        """Check if crypto API is available"""
        try:
            # Simple test to check if we can reach the API
            response = self.tracker.get_price(['bitcoin'], 'usd')
            return bool(response)
        except:
            return False
    
    def get_prices(self, coin_ids, vs_currency='usd'):
        """Get prices for multiple coins - wrapper method"""
        try:
            prices = self.tracker.get_price(coin_ids, vs_currency)
            return prices
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return {}
    
    def get_coin_details(self, coin_id):
        """Get detailed coin information"""
        try:
            data = self.tracker.get_coin_details(coin_id)
            return data
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return None
    
    def get_trending(self):
        """Get trending coins"""
        try:
            data = self.tracker.get_trending()
            return data
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return {'coins': []}
    
    def get_top_coins(self, vs_currency='usd', limit=100, page=1):
        """Get top coins by market cap"""
        try:
            data = self.tracker.get_top_coins(vs_currency, limit, page)
            return data
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return []
    
    def get_market_chart(self, coin_id, vs_currency='usd', days=7):
        """Get market chart data"""
        try:
            data = self.tracker.get_market_chart(coin_id, vs_currency, days)
            return data
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return None
    
    # Flask route methods (kept for compatibility)
    def get_coins(self):
        """List all available cryptocurrencies"""
        data = self.tracker.get_coin_list()
        return jsonify(data)
    
    def get_price(self):
        """Get current prices for specified coins"""
        coin_ids = request.args.get('ids')
        vs_currency = request.args.get('currency', 'usd')
        
        if not coin_ids:
            return jsonify({"error": "Missing 'ids' parameter"}), 400
        
        coin_list = coin_ids.split(',')
        data = self.tracker.get_price(coin_list, vs_currency)
        return jsonify(data)
    
    def get_details(self, coin_id):
        """Get detailed info for a specific coin"""
        data = self.tracker.get_coin_details(coin_id)
        if not data:
            return jsonify({"error": f"Coin '{coin_id}' not found"}), 404
        return jsonify(data)
    
    def get_chart(self, coin_id):
        """Get market chart data for a coin"""
        vs_currency = request.args.get('currency', 'usd')
        days = request.args.get('days', 7)
        
        data = self.tracker.get_market_chart(coin_id, vs_currency, days)
        if not data:
            return jsonify({"error": "Unable to fetch chart data"}), 500
        return jsonify(data)
    
    def get_portfolio(self):
        """View total portfolio value"""
        vs_currency = request.args.get('currency', 'usd')
        portfolio_value = self.tracker.calculate_portfolio_value(vs_currency)
        return jsonify(portfolio_value if portfolio_value else {"message": "Portfolio empty"})
    
    def add_to_portfolio(self):
        """Add coin to portfolio"""
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid or missing JSON body"}), 400
        
        coin_id = data.get('coin_id')
        amount = data.get('amount')
        purchase_price = data.get('purchase_price', None)
        
        if not coin_id or not amount:
            return jsonify({"error": "Missing 'coin_id' or 'amount'"}), 400
        
        self.tracker.add_to_portfolio(coin_id, amount, purchase_price)
        return jsonify({"message": f"Added {amount} {coin_id} to portfolio"}), 201