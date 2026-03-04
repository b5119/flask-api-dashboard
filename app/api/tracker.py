"""
Cryptocurrency Tracker
Handles crypto price tracking and portfolio management
"""

import requests
from datetime import datetime

class CryptoTracker:
    """CoinGecko API wrapper for cryptocurrency tracking"""
    
    def __init__(self):
        self.base_url = 'https://api.coingecko.com/api/v3'
    
    def get_price(self, coin_ids, vs_currency='usd'):
        """Get current prices for coins"""
        try:
            ids = ','.join(coin_ids) if isinstance(coin_ids, list) else coin_ids
            url = f"{self.base_url}/simple/price"
            params = {
                'ids': ids,
                'vs_currencies': vs_currency,
                'include_market_cap': 'true',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"CoinGecko API Error: {e}")
            return {}
    
    def get_coin_list(self):
        """Get list of all coins"""
        try:
            url = f"{self.base_url}/coins/list"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_coin_details(self, coin_id):
        """Get detailed information about a coin"""
        try:
            url = f"{self.base_url}/coins/{coin_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_trending(self):
        """Get trending coins"""
        try:
            url = f"{self.base_url}/search/trending"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return {'coins': []}
    
    def get_top_coins(self, vs_currency='usd', limit=100, page=1):
        """Get top coins by market cap"""
        try:
            url = f"{self.base_url}/coins/markets"
            params = {
                'vs_currency': vs_currency,
                'order': 'market_cap_desc',
                'per_page': limit,
                'page': page,
                'sparkline': 'false',
                'price_change_percentage': '24h,7d'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def get_market_chart(self, coin_id, vs_currency='usd', days=7):
        """Get market chart data"""
        try:
            url = f"{self.base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': vs_currency,
                'days': days
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def calculate_portfolio_value(self, vs_currency='usd'):
        """Calculate total portfolio value"""
        # Placeholder - implement based on your needs
        return None
    
    def add_to_portfolio(self, coin_id, amount, purchase_price=None):
        """Add coin to portfolio"""
        # Placeholder - implement based on your needs
        pass
