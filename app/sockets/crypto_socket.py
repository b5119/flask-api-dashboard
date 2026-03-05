"""Real-time cryptocurrency price updates via WebSocket"""
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import request
import threading
import time

socketio = None

def init_socketio(app):
    """Initialize SocketIO"""
    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
    register_handlers()
    return socketio

def register_handlers():
    """Register WebSocket event handlers"""
    
    @socketio.on('connect', namespace='/crypto')
    def handle_connect():
        """Handle client connection"""
        emit('connected', {'message': 'Connected to crypto price feed'})
        print(f'Client connected: {request.sid}')
    
    @socketio.on('disconnect', namespace='/crypto')
    def handle_disconnect():
        """Handle client disconnection"""
        print(f'Client disconnected: {request.sid}')
    
    @socketio.on('subscribe', namespace='/crypto')
    def handle_subscribe(data):
        """Subscribe to specific coin updates"""
        coins = data.get('coins', [])
        room = ','.join(sorted(coins))
        join_room(room)
        emit('subscribed', {'coins': coins, 'room': room})
    
    @socketio.on('unsubscribe', namespace='/crypto')
    def handle_unsubscribe(data):
        """Unsubscribe from coin updates"""
        coins = data.get('coins', [])
        room = ','.join(sorted(coins))
        leave_room(room)
        emit('unsubscribed', {'coins': coins})

def background_crypto_updates():
    """Background thread for sending crypto updates"""
    from app.api.crypto_api import CryptoAPI
    
    crypto_api = CryptoAPI()
    coins = ['bitcoin', 'ethereum', 'cardano', 'ripple', 'solana', 'polkadot']
    
    while True:
        try:
            prices = crypto_api.get_prices(coins)
            
            if socketio:
                socketio.emit('crypto_update', prices, namespace='/crypto')
            
            time.sleep(30)  # Update every 30 seconds
            
        except Exception as e:
            print(f"Error in crypto updates: {e}")
            time.sleep(60)

def start_background_tasks():
    """Start background update threads"""
    thread = threading.Thread(target=background_crypto_updates)
    thread.daemon = True
    thread.start()
