from flask import Blueprint, request, jsonify
from src.models.assessment import db, Assessment, LibraryContent, NewsletterSubscription
from src.models.user import User
from src.ai.enhanced_query_processor import enhanced_query_processor
from src.ai.ayurveda_astrology_kb import ayurveda_astrology_kb
from datetime import datetime, timedelta
import json
import os

ai_query_bp = Blueprint('ai_query', __name__)

def get_current_season():
    """Determine current season based on month"""
    month = datetime.now().month
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"
    else:
        return "winter"

def get_life_stage(age):
    """Determine life stage based on age"""
    if age < 16:
        return "childhood"
    elif age < 50:
        return "youth"
    else:
        return "maturity"

def generate_ai_response(query, user_constitution=None, user_age=None, current_season=None, symptoms=None, context=None):
    """
    Generate AI response using Enhanced Query Processor with comprehensive knowledge bases:
    - 13 Ayurvedic Constitutions: Complete body type analysis
    - Vedic Astrology: Planetary influences on health
    - Seasonal Guidance: Time-based recommendations
    - Clinical Protocols: Dr. Helen's 44 years of experience
    """
    
    # Prepare user data for the enhanced processor
    user_data = {
        "constitution": user_constitution,
        "age": user_age,
        "symptoms": symptoms or [],
        "context": context or {}
    }
    
    try:
        # Use the enhanced query processor
        response = enhanced_query_processor.process_query(query, user_data)
        
        # Ensure response has required fields
        if not response.get("answer"):
            response["answer"] = f"Thank you for your question about {query}. Let me provide guidance based on Ayurvedic principles and my clinical experience."
        
        # Add standard fields for compatibility
        response.update({
            "source": "Dr. Helen Thomas DC - Enhanced NanoSutracore System",
            "constitution_specific": user_constitution is not None,
            "personalized": bool(user_constitution),
            "clinical_authority": "Dr. Helen Thomas DC - 44 years clinical experience",
            "warning": "This guidance is for educational purposes. Always consult your healthcare provider for medical advice.",
            "system": "Enhanced Query Processor with Ayurvedic & Astrological Intelligence"
        })
        
        return response
        
    except Exception as e:
        # Fallback response if enhanced processor fails
        return {
            "answer": f"I understand your question about {query}. From my 44 years of clinical experience with Ayurveda, let me share some guidance. The key is always to understand your constitution and current imbalances.",
            "source": "Healing Airwaves Clinical Experience - Fallback Mode",
            "constitution_specific": user_constitution is not None,
            "personalized": True,
            "clinical_authority": "Dr. Helen Thomas DC - 44 years experience",
            "recommendations": ["Take constitutional assessment", "Consider pulse diagnosis", "Follow seasonal guidelines"],
            "herbs_supplements": ["Triphala", "Ashwagandha", "Turmeric"],
            "lifestyle_tips": ["Maintain regular routine", "Eat according to constitution", "Practice daily meditation"],
            "warning": "This guidance is for educational purposes. Always consult your healthcare provider for medical advice.",
            "error": f"Enhanced processor temporarily unavailable: {str(e)}"
        }

@ai_query_bp.route('/ask', methods=['POST'])
def ask_ai():
    """Handle AI query requests with subscription validation"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        email = data.get('email')
        user_id = data.get('user_id')
        
        if not query:
            return jsonify({'success': False, 'error': 'Query is required'}), 400
        
        # Check subscription status
        subscription = None
        if email:
            subscription = NewsletterSubscription.query.filter_by(email=email, is_active=True).first()
        
        if not subscription:
            return jsonify({
                'success': False, 
                'error': 'Subscription required',
                'message': 'Please subscribe to access AI guidance from Dr. Helen Thomas DC'
            }), 403
        
        # Get user's constitutional data if available
        user_constitution = None
        user_age = None
        
        if user_id:
            user = User.query.get(user_id)
            if user:
                user_age = user.age
                # Get latest assessment
                latest_assessment = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.created_at.desc()).first()
                if latest_assessment:
                    user_constitution = latest_assessment.primary_dosha
        
        # Generate AI response using enhanced processor
        current_season = get_current_season()
        life_stage = get_life_stage(user_age) if user_age else None
        
        context = {
            'subscription_type': 'premium',
            'life_stage': life_stage,
            'query_timestamp': datetime.now().isoformat()
        }
        
        ai_response = generate_ai_response(
            query=query,
            user_constitution=user_constitution,
            user_age=user_age,
            current_season=current_season,
            context=context
        )
        
        # Log the query for analytics
        try:
            # You could add query logging here
            pass
        except Exception as log_error:
            print(f"Query logging error: {log_error}")
        
        return jsonify({
            'success': True,
            'response': ai_response,
            'user_context': {
                'constitution': user_constitution,
                'age': user_age,
                'season': current_season,
                'life_stage': life_stage
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@ai_query_bp.route('/constitutional-analysis/<constitution>', methods=['GET'])
def get_constitutional_analysis(constitution):
    """Get detailed constitutional analysis"""
    try:
        analysis = ayurveda_astrology_kb.get_constitutional_analysis(constitution)
        
        if "error" in analysis:
            return jsonify({'success': False, 'error': analysis["error"]}), 404
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@ai_query_bp.route('/planetary-guidance/<planet>', methods=['GET'])
def get_planetary_guidance(planet):
    """Get Vedic astrology planetary guidance"""
    try:
        constitution = request.args.get('constitution')
        guidance = ayurveda_astrology_kb.get_planetary_guidance(planet, constitution)
        
        if "error" in guidance:
            return jsonify({'success': False, 'error': guidance["error"]}), 404
        
        return jsonify({
            'success': True,
            'guidance': guidance
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@ai_query_bp.route('/seasonal-recommendations', methods=['GET'])
def get_seasonal_recommendations():
    """Get seasonal health recommendations"""
    try:
        season = request.args.get('season', get_current_season())
        constitution = request.args.get('constitution', 'general')
        
        recommendations = ayurveda_astrology_kb.get_seasonal_recommendations(season, constitution)
        
        if "error" in recommendations:
            return jsonify({'success': False, 'error': recommendations["error"]}), 404
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@ai_query_bp.route('/avatar-script', methods=['POST'])
def get_avatar_script():
    """Generate avatar script for speaking responses"""
    try:
        data = request.get_json()
        response_text = data.get('response_text', '')
        context = data.get('context', 'general')
        
        # Generate speaking script for avatar
        script = {
            "text": response_text,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.65,
                "use_speaker_boost": True
            },
            "speaking_style": "professional_warm",
            "pause_points": [],
            "emphasis_words": ["constitution", "dosha", "Ayurveda", "healing", "balance"]
        }
        
        # Add natural pause points
        sentences = response_text.split('. ')
        for i, sentence in enumerate(sentences):
            if i < len(sentences) - 1:  # Don't add pause after last sentence
                script["pause_points"].append(len('. '.join(sentences[:i+1])) + 2)
        
        return jsonify({
            'success': True,
            'script': script
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@ai_query_bp.route('/subscription-status/<email>', methods=['GET'])
def check_subscription_status(email):
    """Check subscription status for email"""
    try:
        subscription = NewsletterSubscription.query.filter_by(email=email, is_active=True).first()
        
        return jsonify({
            'success': True,
            'subscribed': subscription is not None,
            'subscription_date': subscription.created_at.isoformat() if subscription else None
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e)
        }), 500

# Newsletter subscription endpoint
@ai_query_bp.route('/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter for AI access"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        # Check if already subscribed
        existing = NewsletterSubscription.query.filter_by(email=email).first()
        
        if existing:
            if existing.is_active:
                return jsonify({
                    'success': True,
                    'message': 'Already subscribed',
                    'subscription_date': existing.created_at.isoformat()
                })
            else:
                # Reactivate subscription
                existing.is_active = True
                existing.updated_at = datetime.utcnow()
                db.session.commit()
                
                return jsonify({
                    'success': True,
                    'message': 'Subscription reactivated',
                    'subscription_date': existing.updated_at.isoformat()
                })
        
        # Create new subscription
        subscription = NewsletterSubscription(
            email=email,
            is_active=True,
            subscription_source='ai_query_access'
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Successfully subscribed! You now have access to AI guidance.',
            'subscription_date': subscription.created_at.isoformat()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Subscription failed',
            'message': str(e)
        }), 500
