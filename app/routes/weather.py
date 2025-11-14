"""
Weather Routes
"""
from flask import Blueprint, render_template, jsonify, request
from app.api.weather_api import WeatherAPI

weather_bp = Blueprint('weather', __name__)
weather_api = WeatherAPI()

@weather_bp.route('/')
def index():
    """Weather home page"""
    return render_template('weather.html',
                         title='Weather',
                         active_page='weather',
                         city='London')

@weather_bp.route('/home')
def weather_home():
    """Alias for weather home (required by templates)"""
    return index()

@weather_bp.route('/api/current/<city>')
def api_current(city):
    """API endpoint for current weather"""
    units = request.args.get('units', 'metric')
    result = weather_api.get_current_weather(city, units=units)
    
    if result:
        return jsonify({'success': True, 'weather': result})
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch weather data'}), 400

@weather_bp.route('/api/forecast/<city>')
def api_forecast(city):
    """API endpoint for weather forecast"""
    days = int(request.args.get('days', 5))
    units = request.args.get('units', 'metric')
    result = weather_api.get_forecast(city, days=days, units=units)
    
    if result:
        return jsonify({'success': True, 'forecast': result})
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch forecast data'}), 400
