"""
Notification Routes
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import NotificationLog
from app.api.notification_api import NotificationAPI

notifications_bp = Blueprint('notifications', __name__)
notification_api = NotificationAPI()


@notifications_bp.route('/')
@login_required
def index():
    """Notifications home page"""
    return render_template('notifications.html',
                         title='Notifications',
                         active_page='notifications')


@notifications_bp.route('/send-email', methods=['POST'])
@login_required
def send_email():
    """Send email notification"""
    data = request.get_json()
    
    to_email = data.get('to_email')
    subject = data.get('subject')
    message = data.get('message')
    is_html = data.get('is_html', False)
    
    if not all([to_email, subject, message]):
        return jsonify({
            'success': False,
            'error': 'Missing required fields'
        }), 400
    
    try:
        success = notification_api.send_email(
            to_email=to_email,
            subject=subject,
            content=message,
            content_type='text/html' if is_html else 'text/plain'
        )
        
        log = NotificationLog(
            user_id=current_user.id,
            notification_type='email',
            recipient=to_email,
            subject=subject,
            message=message,
            status='sent' if success else 'failed'
        )
        db.session.add(log)
        db.session.commit()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Email sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send email'
            }), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@notifications_bp.route('/send-sms', methods=['POST'])
@login_required
def send_sms():
    """Send SMS notification"""
    data = request.get_json()
    
    to_number = data.get('to_number')
    message = data.get('message')
    
    if not all([to_number, message]):
        return jsonify({
            'success': False,
            'error': 'Missing required fields'
        }), 400
    
    try:
        success = notification_api.send_sms(
            to_number=to_number,
            message=message
        )
        
        log = NotificationLog(
            user_id=current_user.id,
            notification_type='sms',
            recipient=to_number,
            message=message,
            status='sent' if success else 'failed'
        )
        db.session.add(log)
        db.session.commit()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'SMS sent successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to send SMS'
            }), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@notifications_bp.route('/api/history')
@login_required
def api_history():
    """Get notification history via API"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    notification_type = request.args.get('type')
    
    query = current_user.notification_logs
    
    if notification_type:
        query = query.filter_by(notification_type=notification_type)
    
    logs = query.order_by(NotificationLog.sent_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'logs': [{
            'id': log.id,
            'type': log.notification_type,
            'recipient': log.recipient,
            'subject': log.subject,
            'status': log.status,
            'sent_at': log.sent_at.isoformat() if log.sent_at else None
        } for log in logs.items],
        'total': logs.total,
        'pages': logs.pages,
        'current_page': logs.page
    })