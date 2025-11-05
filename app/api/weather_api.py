#!/usr/bin/env python3
"""
Flask API Integration for Weather & Air Quality Dashboard
Uses: OpenWeatherMap + AirVisual APIs
Author: FRANKLAUS
"""

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from datetime import datetime
import requests
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ============================
# Core WeatherDashboard Class
# ============================

class WeatherDashboard:
    def __init__(self):
        self.openweather_key = os.getenv('OPENWEATHER_API_KEY')
        self.airvisual_key = os.getenv('AIRVISUAL_API_KEY')
        self.openweather_base = 'https://api.openweathermap.org/data/2.5'
        self.airvisual_base = 'https://api.airvisual.com/v2'
        
        if not self.openweather_key:
            print("⚠️ OPENWEATHER_API_KEY not found in environment!")

    def get_current_weather(self, city, units='metric'):
        """Fetch current weather for a given city."""
        endpoint = f"{self.openweather_base}/weather"
        params = {'q': city, 'appid': self.openweather_key, 'units': units}

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
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'weather': data['weather'][0]['main'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind'].get('deg', 0),
                'clouds': data['clouds']['all'],
                'visibility': data.get('visibility', 0),
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).isoformat(),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).isoformat(),
                'timezone': data['timezone'],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}

    def get_forecast(self, city, days=5, units='metric'):
        """Fetch weather forecast for a city."""
        endpoint = f"{self.openweather_base}/forecast"
        params = {
            'q': city,
            'appid': self.openweather_key,
            'units': units,
            'cnt': days * 8
        }

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            forecast = {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'forecasts': []
            }

            for item in data['list']:
                forecast['forecasts'].append({
                    'datetime': datetime.fromtimestamp(item['dt']).isoformat(),
                    'temperature': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'pressure': item['main']['pressure'],
                    'humidity': item['main']['humidity'],
                    'weather': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed'],
                    'clouds': item['clouds']['all'],
                    'pop': item.get('pop', 0) * 100
                })
            return forecast
        except Exception as e:
            return {'error': str(e)}

    def get_air_quality(self, city, state=None, country=None):
        """Fetch air quality data."""
        endpoint = f"{self.airvisual_base}/city"
        params = {'city': city, 'key': self.airvisual_key}
        if state: params['state'] = state
        if country: params['country'] = country

        try:
            response = requests.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data['status'] != 'success':
                return {'error': data.get('message', 'Unknown API error')}
            
            current = data['data']['current']
            pollution = current['pollution']
            weather = current['weather']
            return {
                'city': data['data']['city'],
                'state': data['data']['state'],
                'country': data['data']['country'],
                'aqi_us': pollution['aqius'],
                'main_pollutant_us': pollution['mainus'],
                'aqi_cn': pollution['aqicn'],
                'main_pollutant_cn': pollution['maincn'],
                'temperature': weather['tp'],
                'humidity': weather['hu'],
                'wind_speed': weather['ws'],
                'timestamp': pollution['ts']
            }
        except Exception as e:
            return {'error': str(e)}

    def compare_cities(self, cities, units='metric'):
        """Compare multiple cities."""
        results = []
        for city in cities:
            weather = self.get_current_weather(city, units)
            results.append(weather)
        return {'comparison': results}


dashboard = WeatherDashboard()

# =======================
# Flask API Endpoints
# =======================

@app.route('/')
def index():
    return jsonify({
        'message': '🌤️ Weather & Air Quality Flask API',
        'endpoints': {
            '/weather?city=CityName': 'Get current weather',
            '/forecast?city=CityName&days=5': 'Get forecast',
            '/air-quality?city=CityName': 'Get air quality data',
            '/compare?cities=City1,City2': 'Compare multiple cities'
        }
    })


@app.route('/weather')
def weather_route():
    city = request.args.get('city')
    units = request.args.get('units', 'metric')
    if not city:
        return jsonify({'error': 'Missing city parameter'}), 400
    result = dashboard.get_current_weather(city, units)
    return jsonify(result)


@app.route('/forecast')
def forecast_route():
    city = request.args.get('city')
    days = int(request.args.get('days', 5))
    units = request.args.get('units', 'metric')
    if not city:
        return jsonify({'error': 'Missing city parameter'}), 400
    result = dashboard.get_forecast(city, days, units)
    return jsonify(result)


@app.route('/air-quality')
def air_quality_route():
    city = request.args.get('city')
    state = request.args.get('state')
    country = request.args.get('country')
    if not city:
        return jsonify({'error': 'Missing city parameter'}), 400
    result = dashboard.get_air_quality(city, state, country)
    return jsonify(result)


@app.route('/compare')
def compare_route():
    cities_param = request.args.get('cities')
    units = request.args.get('units', 'metric')
    if not cities_param:
        return jsonify({'error': 'Missing cities parameter'}), 400
    cities = [c.strip() for c in cities_param.split(',')]
    result = dashboard.compare_cities(cities, units)
    return jsonify(result)


# =======================
# Flask App Entry Point
# =======================

if __name__ == '__main__':
    app.run(debug=True)
