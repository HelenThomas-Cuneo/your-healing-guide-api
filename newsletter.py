from flask import Blueprint, jsonify, request
from src.models.assessment import NewsletterSubscription, db
from datetime import datetime
import re

newsletter_bp = Blueprint('newsletter', __name__)

@newsletter_bp.route('/api/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter and lead magnet"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        email = data['email'].strip().lower()
        source = data.get('source', 'unknown')
        
        # Validate email format
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Check if email already exists
        existing_subscription = NewsletterSubscription.query.filter_by(email=email).first()
        
        if existing_subscription:
            # Update existing subscription
            existing_subscription.source = source
            existing_subscription.subscribed_at = datetime.utcnow()
            existing_subscription.is_active = True
        else:
            # Create new subscription
            subscription = NewsletterSubscription(
                email=email,
                source=source,
                subscribed_at=datetime.utcnow(),
                is_active=True
            )
            db.session.add(subscription)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Successfully subscribed to newsletter',
            'download_url': '/api/lead-magnet/download'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Subscription failed: {str(e)}'}), 500

@newsletter_bp.route('/api/newsletter/unsubscribe', methods=['POST'])
def unsubscribe_newsletter():
    """Unsubscribe from newsletter"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'error': 'Email is required'}), 400
        
        email = data['email'].strip().lower()
        
        subscription = NewsletterSubscription.query.filter_by(email=email).first()
        
        if subscription:
            subscription.is_active = False
            subscription.unsubscribed_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Successfully unsubscribed from newsletter'
            }), 200
        else:
            return jsonify({'error': 'Email not found in subscription list'}), 404
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Unsubscribe failed: {str(e)}'}), 500

@newsletter_bp.route('/api/newsletter/stats', methods=['GET'])
def get_newsletter_stats():
    """Get newsletter subscription statistics"""
    try:
        total_subscribers = NewsletterSubscription.query.filter_by(is_active=True).count()
        total_unsubscribed = NewsletterSubscription.query.filter_by(is_active=False).count()
        
        # Get subscribers by source
        lead_magnet_subs = NewsletterSubscription.query.filter_by(
            source='lead_magnet_13_body_types', 
            is_active=True
        ).count()
        
        stats = {
            'total_active_subscribers': total_subscribers,
            'total_unsubscribed': total_unsubscribed,
            'lead_magnet_subscribers': lead_magnet_subs,
            'conversion_rate': f"{(lead_magnet_subs / max(total_subscribers, 1) * 100):.1f}%"
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get stats: {str(e)}'}), 500
