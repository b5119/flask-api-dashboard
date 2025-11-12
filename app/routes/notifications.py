"""
Notifications Routes
Handles notification-related endpoints (in-memory storage for demo)
"""

from flask import Blueprint, jsonify, request
from datetime import datetime

notifications_bp = Blueprint('notifications', __name__)

# In-memory storage for demo (use database in production)
notifications_store = []
notification_id_counter = 1

@notifications_bp.route('/', methods=['GET'])
def get_notifications():
    """Get all notifications"""
    return jsonify({
        'success': True,
        'notifications': notifications_store,
        'count': len(notifications_store)
    })

@notifications_bp.route('/', methods=['POST'])
def create_notification():
    """Create a new notification"""
    global notification_id_counter
    
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            'success': False,
            'error': 'Message is required'
        }), 400
    
    notification = {
        'id': notification_id_counter,
        'message': data['message'],
        'type': data.get('type', 'info'),
        'read': False,
        'created_at': datetime.utcnow().isoformat()
    }
    
    notifications_store.append(notification)
    notification_id_counter += 1
    
    return jsonify({
        'success': True,
        'notification': notification
    }), 201

@notifications_bp.route('/<int:notification_id>', methods=['GET'])
def get_notification(notification_id):
    """Get a specific notification"""
    notification = next((n for n in notifications_store if n['id'] == notification_id), None)
    
    if not notification:
        return jsonify({
            'success': False,
            'error': 'Notification not found'
        }), 404
    
    return jsonify({
        'success': True,
        'notification': notification
    })

@notifications_bp.route('/<int:notification_id>', methods=['PUT', 'PATCH'])
def update_notification(notification_id):
    """Mark notification as read/unread"""
    notification = next((n for n in notifications_store if n['id'] == notification_id), None)
    
    if not notification:
        return jsonify({
            'success': False,
            'error': 'Notification not found'
        }), 404
    
    data = request.get_json()
    notification['read'] = data.get('read', True)
    
    return jsonify({
        'success': True,
        'notification': notification
    })

@notifications_bp.route('/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a notification"""
    global notifications_store
    
    notification = next((n for n in notifications_store if n['id'] == notification_id), None)
    
    if not notification:
        return jsonify({
            'success': False,
            'error': 'Notification not found'
        }), 404
    
    notifications_store = [n for n in notifications_store if n['id'] != notification_id]
    
    return jsonify({
        'success': True,
        'message': 'Notification deleted'
    })

@notifications_bp.route('/clear', methods=['DELETE'])
def clear_notifications():
    """Clear all notifications"""
    global notifications_store
    count = len(notifications_store)
    notifications_store = []
    
    return jsonify({
        'success': True,
        'message': f'{count} notification(s) cleared'
    })

@notifications_bp.route('/unread', methods=['GET'])
def get_unread_notifications():
    """Get unread notifications"""
    unread = [n for n in notifications_store if not n['read']]
    
    return jsonify({
        'success': True,
        'notifications': unread,
        'count': len(unread)
    })

@notifications_bp.route('/mark-all-read', methods=['PUT'])
def mark_all_read():
    """Mark all notifications as read"""
    for notification in notifications_store:
        notification['read'] = True
    
    return jsonify({
        'success': True,
        'message': 'All notifications marked as read'
    })