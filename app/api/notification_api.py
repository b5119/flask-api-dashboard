#!/usr/bin/env python3
"""
Flask API Integration for Notification System
Endpoints for sending Email and SMS via SendGrid and Twilio
"""

import os
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# ============================================
# Notification System Core Class
# ============================================
class NotificationSystem:
    def __init__(self):
        self.sendgrid_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL')
        self.twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
        
        self.email_enabled = bool(self.sendgrid_key and self.from_email)
        self.sms_enabled = bool(self.twilio_sid and self.twilio_token and self.twilio_number)

    def send_email(self, to_email, subject, content, content_type='text/plain'):
        """Send email using SendGrid"""
        if not self.email_enabled:
            return {"success": False, "error": "Email not configured"}
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
            if response.status_code in [200, 201, 202]:
                return {"success": True, "message": f"Email sent to {to_email}"}
            else:
                return {"success": False, "error": f"Status {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def send_sms(self, to_number, message):
        """Send SMS using Twilio"""
        if not self.sms_enabled:
            return {"success": False, "error": "SMS not configured"}
        try:
            from twilio.rest import Client
            client = Client(self.twilio_sid, self.twilio_token)
            msg = client.messages.create(body=message, from_=self.twilio_number, to=to_number)
            return {"success": True, "message": f"SMS sent to {to_number}", "sid": msg.sid}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def load_template(self, template_name):
        """Load email template"""
        path = f"templates/{template_name}.html"
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None

    def format_template(self, template, **kwargs):
        """Inject variables into template"""
        try:
            return template.format(**kwargs)
        except Exception as e:
            return None


notifier = NotificationSystem()

# ============================================
# API ROUTES
# ============================================

@app.route('/')
def home():
    return jsonify({
        "service": "Notification System API",
        "email_enabled": notifier.email_enabled,
        "sms_enabled": notifier.sms_enabled,
        "endpoints": {
            "POST /send-email": "Send email via SendGrid",
            "POST /send-sms": "Send SMS via Twilio",
            "POST /send-bulk-email": "Send bulk emails (JSON list)",
            "POST /send-bulk-sms": "Send bulk SMS (JSON list)",
            "POST /send-template": "Send templated email"
        }
    })


@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    content = data.get('message')
    html = data.get('html', False)

    if not all([to_email, subject, content]):
        return jsonify({"error": "Missing required fields"}), 400

    content_type = 'text/html' if html else 'text/plain'
    result = notifier.send_email(to_email, subject, content, content_type)
    return jsonify(result)


@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    to_number = data.get('to')
    message = data.get('message')

    if not all([to_number, message]):
        return jsonify({"error": "Missing required fields"}), 400

    result = notifier.send_sms(to_number, message)
    return jsonify(result)


@app.route('/send-bulk-email', methods=['POST'])
def send_bulk_email():
    data = request.get_json()
    recipients = data.get('recipients', [])
    subject = data.get('subject')
    content = data.get('message')
    html = data.get('html', False)

    if not recipients or not subject or not content:
        return jsonify({"error": "Missing recipients, subject, or message"}), 400

    content_type = 'text/html' if html else 'text/plain'
    results = []
    for r in recipients:
        results.append(notifier.send_email(r, subject, content, content_type))
    return jsonify({"results": results})


@app.route('/send-bulk-sms', methods=['POST'])
def send_bulk_sms():
    data = request.get_json()
    recipients = data.get('recipients', [])
    message = data.get('message')

    if not recipients or not message:
        return jsonify({"error": "Missing recipients or message"}), 400

    results = []
    for r in recipients:
        results.append(notifier.send_sms(r, message))
    return jsonify({"results": results})


@app.route('/send-template', methods=['POST'])
def send_template():
    data = request.get_json()
    to_email = data.get('to')
    subject = data.get('subject')
    template_name = data.get('template')
    variables = data.get('variables', {})

    if not all([to_email, subject, template_name]):
        return jsonify({"error": "Missing required fields"}), 400

    template_content = notifier.load_template(template_name)
    if not template_content:
        return jsonify({"error": f"Template '{template_name}' not found"}), 404

    formatted = notifier.format_template(template_content, **variables)
    if not formatted:
        return jsonify({"error": "Error formatting template"}), 400

    result = notifier.send_email(to_email, subject, formatted, content_type='text/html')
    return jsonify(result)


# ============================================
# APP START
# ============================================
if __name__ == '__main__':
    app.run(debug=True, port=5001)
