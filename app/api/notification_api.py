#!/usr/bin/env python3
"""
Flask API Integration for Notification System
Notification handler class for sending Email and SMS via SendGrid and Twilio
"""

import os
from datetime import datetime

class NotificationAPI:
    """Notification API handler class"""
    
    def __init__(self):
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL')
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        self.email_enabled = bool(self.sendgrid_key and self.from_email)
        self.sms_enabled = bool(self.twilio_sid and self.twilio_token and self.twilio_number)
def send_email(self, to_email, subject, content, content_type='text/plain'):
    """Send email using SendGrid - returns boolean"""
    if not self.email_enabled:
        return False
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email,
            subject=subject,
            plain_text_content=content if content_type == 'text/plain' else None,
            html_content=content if content_type == 'text/html' else None
        )
        sg = SendGridAPIClient(self.sendgrid_key)
        response = sg.send(message)
        return response.status_code in [200, 201, 202]
    except Exception as e:
        print(f"Email Error: {e}")
        return False

def send_sms(self, to_number, message):
    """Send SMS using Twilio - returns boolean"""
    if not self.sms_enabled:
        return False
    try:
        from twilio.rest import Client
        client = Client(self.twilio_sid, self.twilio_token)
        msg = client.messages.create(body=message, from_=self.twilio_number, to=to_number)
        return bool(msg.sid)
    except Exception as e:
        print(f"SMS Error: {e}")
        return False