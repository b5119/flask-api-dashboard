"""
Weather Routes
"""

from flask import Blueprint, render_template, request, jsonify
from app.api.weather_api import WeatherAPI

weather_bp = Blueprint('weather', __name__)
weather_api = WeatherAPI()


@weather_bp.route('/')
def index():
    """Weather home page"""
    city = request.args.get('city', 'London')
    
    return render_template('weather.html',
                         title='Weather',
                         active_page='weather',
                         city=city)


@weather_bp.route('/api/current/<city>')
def get_current_weather(city):
    """Get current weather for a city"""
    units = request.args.get('units', 'metric')
    
    try:
        weather = weather_api.get_current_weather(city, units)
        
        if weather:
            return jsonify({
                'success': True,
                'weather': weather
            })
        else:
            return jsonify({
                'success': False,
                'error': 'City not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@weather_bp.route('/api/forecast/<city>')
def get_forecast(city):
    """Get weather forecast"""
    days = request.args.get('days', 5, type=int)
    units = request.args.get('units', 'metric')
    
    try:
        forecast = weather_api.get_forecast(city, days, units)
        
        if forecast:
            return jsonify({
                'success': True,
                'forecast': forecast
            })
        else:
            return jsonify({
                'success': False,
                'error': 'City not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@weather_bp.route('/api/air-quality/<city>')
def get_air_quality(city):
    """Get air quality data"""
    state = request.args.get('state')
    country = request.args.get('country')
    
    try:
        air_quality = weather_api.get_air_quality(city, state, country)
        
        if air_quality:
            return jsonify({
                'success': True,
                'air_quality': air_quality
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Data not available'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@weather_bp.route('/compare')
def compare_cities():
    """Compare weather in multiple cities"""
    cities = request.args.getlist('cities')
    
    if not cities:
        cities = ['London', 'New York', 'Tokyo']
    
    return render_template('weather_compare.html',
                         title='Compare Weather',
                         active_page='weather',
                         cities=cities)


@weather_bp.route('/api/compare')
def api_compare_cities():
    """Compare weather via API"""
    cities = request.args.getlist('cities')
    units = request.args.get('units', 'metric')
    
    if not cities:
        return jsonify({
            'success': False,
            'error': 'No cities provided'
        }), 400
    
    try:
        results = []
        for city in cities:
            weather = weather_api.get_current_weather(city, units)
            if weather:
                results.append(weather)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500