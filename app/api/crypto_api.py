"""
Cryptocurrency API - Standalone version using CoinGecko API directly
"""

import requests

class CryptoAPI:
    """Crypto API handler class - uses CoinGecko API (no API key required)"""
    
    def __init__(self):
        self.base_url = 'https://api.coingecko.com/api/v3'
    
    def check_status(self):
        """Check if crypto API is available"""
        try:
            response = requests.get(f'{self.base_url}/ping', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_prices(self, coin_ids, vs_currency='usd'):
        """Get prices for multiple coins"""
        try:
            # Convert list to comma-separated string
            if isinstance(coin_ids, list):
                coin_ids = ','.join(coin_ids)
            
            url = f'{self.base_url}/simple/price'
            params = {
                'ids': coin_ids,
                'vs_currencies': vs_currency,
                'include_24hr_change': 'true',
                'include_market_cap': 'true',
                'include_24h_vol': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Reformat data to match expected structure
            result = {}
            for coin_id, coin_data in data.items():
                result[coin_id] = {
                    'usd': coin_data.get(vs_currency, 0),
                    'usd_24h_change': coin_data.get(f'{vs_currency}_24h_change', 0),
                    'usd_market_cap': coin_data.get(f'{vs_currency}_market_cap', 0),
                    'usd_24h_vol': coin_data.get(f'{vs_currency}_24h_vol', 0)
                }
            
            return result
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return {}
    
    def get_coin_details(self, coin_id):
        """Get detailed coin information"""
        try:
            url = f'{self.base_url}/coins/{coin_id}'
            params = {
                'localization': 'false',
                'tickers': 'false',
                'market_data': 'true',
                'community_data': 'false',
                'developer_data': 'false'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            market_data = data.get('market_data', {})
            
            return {
                'id': data.get('id'),
                'symbol': data.get('symbol', '').upper(),
                'name': data.get('name'),
                'image': data.get('image', {}).get('large'),
                'current_price': market_data.get('current_price', {}).get('usd'),
                'market_cap': market_data.get('market_cap', {}).get('usd'),
                'market_cap_rank': data.get('market_cap_rank'),
                'total_volume': market_data.get('total_volume', {}).get('usd'),
                'high_24h': market_data.get('high_24h', {}).get('usd'),
                'low_24h': market_data.get('low_24h', {}).get('usd'),
                'price_change_24h': market_data.get('price_change_24h'),
                'price_change_percentage_24h': market_data.get('price_change_percentage_24h'),
                'circulating_supply': market_data.get('circulating_supply'),
                'total_supply': market_data.get('total_supply')
            }
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return None
    
    def get_trending(self):
        """Get trending coins"""
        try:
            url = f'{self.base_url}/search/trending'
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'coins': data.get('coins', [])
            }
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return {'coins': []}
    
    def get_top_coins(self, vs_currency='usd', limit=100, page=1):
        """Get top coins by market cap"""
        try:
            url = f'{self.base_url}/coins/markets'
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
            data = response.json()
            
            return data
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return []
    
    def get_market_chart(self, coin_id, vs_currency='usd', days=7):
        """Get market chart data"""
        try:
            url = f'{self.base_url}/coins/{coin_id}/market_chart'
            params = {
                'vs_currency': vs_currency,
                'days': days
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'prices': data.get('prices', []),
                'market_caps': data.get('market_caps', []),
                'total_volumes': data.get('total_volumes', [])
            }
        except Exception as e:
            print(f"Crypto API Error: {e}")
            return None