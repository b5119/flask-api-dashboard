"""Test API endpoints"""
import pytest
from app import create_app

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code in [200, 503]
    data = response.get_json()
    assert 'status' in data
    assert 'services' in data

def test_dashboard_data(client):
    """Test dashboard data endpoint"""
    response = client.get('/dashboard/data')
    assert response.status_code == 200

def test_news_api(client):
    """Test news API"""
    response = client.get('/news/api/headlines?category=general&country=us&page=1')
    assert response.status_code == 200

def test_weather_api(client):
    """Test weather API"""
    response = client.get('/weather/api/current/London')
    assert response.status_code == 200

def test_crypto_api(client):
    """Test crypto API"""
    response = client.get('/crypto/api/prices?coins=bitcoin')
    assert response.status_code == 200
