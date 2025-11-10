"""
Weather Routes
Handles weather-related endpoints
"""

from flask import Blueprint, jsonify, request
from app.api.weather_api import WeatherAPI

weather_bp = Blueprint('weather', __name__)
weather_api = WeatherAPI()

@weather_bp.route('/current', methods=['GET'])
def get_current_weather():
    """Get current weather for a location"""
    city = request.args.get('city')
    units = request.args.get('units', 'metric')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    result = weather_api.get_current_weather(city, units=units)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to fetch weather data'}), 400

@weather_bp.route('/forecast', methods=['GET'])
def get_forecast():
    """Get weather forecast for a location"""
    city = request.args.get('city')
    days = int(request.args.get('days', 5))
    units = request.args.get('units', 'metric')
    
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400
    
    result = weather_api.get_forecast(city, days=days, units=units)
    
    if result:
        return jsonify(result)
    else:
        return jsonify({'error': 'Failed to fetch forecast data'}), 400

@weather_bp.route('/status', methods=['GET'])
def check_status():
    """Check if Weather API is configured"""
    is_configured = weather_api.check_status()
    
    return jsonify({
        'configured': is_configured,
        'message': 'Weather API is configured' if is_configured else 'Weather API key not found'
    })