"""
News API Wrapper
Wraps NewsAPI functionality for Flask application
"""

import requests
import os
from flask import current_app

class NewsAPI:
    def __init__(self):
        # Only use environment variable during initialization
        self.api_key = os.getenv('NEWSAPI_KEY')
        self.base_url = 'https://newsapi.org/v2'
    
    def _get_api_key(self):
        """Get API key from env or Flask config (when in app context)"""
        if self.api_key:
            return self.api_key
        
        # Try to get from Flask config if in app context
        try:
            return current_app.config.get('NEWSAPI_KEY')
        except RuntimeError:
            # Not in app context
            return None
    
    def check_status(self):
        """Check if API is configured and available"""
        return bool(self._get_api_key())
    
    def get_top_headlines(self, country='us', category=None, query=None, page=1, page_size=20):
        """Get top headlines"""
        api_key = self._get_api_key()
        if not api_key:
            return {'articles': [], 'totalResults': 0}
        
        endpoint = f"{self.base_url}/top-headlines"
        params = {
            'apiKey': api_key,
            'country': country,
            'page': page,
            'pageSize': page_size
        }
        
        if category:
            params['category'] = category
        if query:
            params['q'] = query
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"News API Error: {e}")
            return {'articles': [], 'totalResults': 0}
    
    def search_everything(self, query, from_date=None, to_date=None, language='en', 
                         sort_by='publishedAt', page=1, page_size=20):
        """Search all news articles"""
        api_key = self._get_api_key()
        if not api_key:
            return {'articles': [], 'totalResults': 0}
        
        endpoint = f"{self.base_url}/everything"
        params = {
            'apiKey': api_key,
            'q': query,
            'language': language,
            'sortBy': sort_by,
            'page': page,
            'pageSize': page_size
        }
        
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"News API Error: {e}")
            return {'articles': [], 'totalResults': 0}
    
    def get_sources(self, category=None, language='en', country=None):
        """Get available news sources"""
        api_key = self._get_api_key()
        if not api_key:
            return []
        
        endpoint = f"{self.base_url}/top-headlines/sources"
        params = {
            'apiKey': api_key,
            'language': language
        }
        
        if category:
            params['category'] = category
        if country:
            params['country'] = country
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('sources', [])
        except Exception as e:
            print(f"News API Error: {e}")
            return []
    
    def search(self, query, page_size=10):
        """Simple search wrapper for dashboard"""
        return self.search_everything(query, page_size=page_size)