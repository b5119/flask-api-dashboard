"""
Weather API Wrapper
Wraps OpenWeatherMap API functionality for Flask application
"""

import requests
import os
from flask import current_app
from datetime import datetime

class WeatherAPI:
    def __init__(self):
        # Only use environment variable during initialization
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
    
    def _get_api_key(self):
        """Get API key from env or Flask config (when in app context)"""
        if self.api_key:
            return self.api_key
        
        # Try to get from Flask config if in app context
        try:
            return current_app.config.get('OPENWEATHER_API_KEY')
        except RuntimeError:
            # Not in app context
            return None
    
    def check_status(self):
        """Check if API is configured"""
        return bool(self._get_api_key())
    
    def get_current_weather(self, city, units='metric'):
        """Get current weather for a city"""
        api_key = self._get_api_key()
        if not api_key:
            return None
        
        endpoint = f"{self.base_url}/weather"
        params = {
            'q': city,
            'appid': api_key,
            'units': units
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind'].get('deg', 0),
                'clouds': data['clouds']['all'],
                'visibility': data.get('visibility', 0),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Weather API Error: {e}")
            return None
    
    def get_forecast(self, city, days=5, units='metric'):
        """Get weather forecast"""
        api_key = self._get_api_key()
        if not api_key:
            return None
        
        endpoint = f"{self.base_url}/forecast"
        params = {
            'q': city,
            'appid': api_key,
            'units': units,
            'cnt': days * 8
        }
        
        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            for item in data['list']:
                forecasts.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'humidity': item['main']['humidity'],
                    'weather': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'wind_speed': item['wind']['speed'],
                    'clouds': item['clouds']['all'],
                    'pop': item.get('pop', 0) * 100
                })
            
            return {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'forecasts': forecasts
            }
        except Exception as e:
            print(f"Weather API Error: {e}")
            return None
    
    def get_air_quality(self, city, state=None, country=None):
        """Get air quality data (placeholder - requires AirVisual API)"""
        # This would require AirVisual API integration
        return None