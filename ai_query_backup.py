from flask import Blueprint, request, jsonify
from src.models.assessment import db, Assessment, LibraryContent, NewsletterSubscription
from src.models.user import User
from src.ai.enhanced_query_processor import enhanced_query_processor
from src.ai.ayurveda_astrology_kb import ayurveda_astrology_kb
from datetime import datetime, timedelta
import json
import os

ai_query_bp = Blueprint('ai_query', __name__)

# Ayurvedic knowledge base for AI responses
AYURVEDIC_KNOWLEDGE = {
    "constitutions": {
        "vata": {
            "elements": ["air", "space"],
            "qualities": ["dry", "light", "cold", "rough", "subtle", "mobile"],
            "signs_symptoms": {
                "balanced": ["creative", "enthusiastic", "flexible", "quick thinking"],
                "imbalanced": ["anxiety", "insomnia", "dry skin", "constipation", "joint pain", "restlessness"]
            },
            "diet": {
                "favor": ["warm", "moist", "heavy", "sweet", "sour", "salty"],
                "avoid": ["cold", "dry", "light", "bitter", "pungent", "astringent"],
                "foods": ["cooked grains", "warm milk", "ghee", "nuts", "dates", "avocado"]
            },
            "lifestyle": ["regular routine", "oil massage", "warm baths", "gentle exercise", "meditation"],
            "seasons": {
                "fall_winter": "Most vulnerable, need extra warmth and grounding",
                "spring_summer": "More balanced, can handle lighter foods"
            }
        },
        "pitta": {
            "elements": ["fire", "water"],
            "qualities": ["hot", "sharp", "light", "liquid", "mobile", "oily"],
            "signs_symptoms": {
                "balanced": ["intelligent", "focused", "confident", "good digestion"],
                "imbalanced": ["anger", "inflammation", "acidity", "skin rashes", "excessive heat"]
            },
            "diet": {
                "favor": ["cool", "sweet", "bitter", "astringent"],
                "avoid": ["hot", "spicy", "sour", "salty", "pungent"],
                "foods": ["cooling fruits", "leafy greens", "coconut", "cucumber", "mint"]
            },
            "lifestyle": ["avoid overheating", "moderate exercise", "cooling practices", "avoid competition"],
            "seasons": {
                "summer": "Most vulnerable, need cooling foods and practices",
                "winter": "More balanced, can handle warming foods"
            }
        },
        "kapha": {
            "elements": ["earth", "water"],
            "qualities": ["heavy", "slow", "cold", "oily", "smooth", "stable"],
            "signs_symptoms": {
                "balanced": ["calm", "strong", "compassionate", "stable"],
                "imbalanced": ["lethargy", "weight gain", "congestion", "depression", "attachment"]
            },
            "diet": {
                "favor": ["light", "warm", "dry", "pungent", "bitter", "astringent"],
                "avoid": ["heavy", "cold", "oily", "sweet", "sour", "salty"],
                "foods": ["spices", "light grains", "vegetables", "legumes", "honey"]
            },
            "lifestyle": ["vigorous exercise", "stimulating activities", "dry brushing", "early rising"],
            "seasons": {
                "spring": "Most vulnerable, need detoxifying and energizing practices",
                "fall": "More balanced, can handle heavier foods"
            }
        }
    },
    
    "life_cycles": {
        "childhood": {
            "dominant_dosha": "kapha",
            "characteristics": ["growth", "immunity building", "learning"],
            "diet": ["warm milk", "ghee", "sweet fruits", "easy to digest foods"],
            "lifestyle": ["regular sleep", "play", "learning", "protection from cold"]
        },
        "adulthood": {
            "dominant_dosha": "pitta",
            "characteristics": ["achievement", "metabolism", "responsibility"],
            "diet": ["balanced nutrition", "regular meals", "avoid excessive heat"],
            "lifestyle": ["work-life balance", "moderate exercise", "stress management"]
        },
        "elderly": {
            "dominant_dosha": "vata",
            "characteristics": ["wisdom", "lightness", "dryness"],
            "diet": ["warm", "nourishing", "easy to digest", "healthy fats"],
            "lifestyle": ["gentle exercise", "oil massage", "regular routine", "spiritual practices"]
        }
    },
    
    "seasons": {
        "spring": {
            "dominant_dosha": "kapha",
            "recommendations": ["detox", "light foods", "exercise", "avoid heavy/oily foods"],
            "herbs": ["turmeric", "ginger", "triphala"]
        },
        "summer": {
            "dominant_dosha": "pitta",
            "recommendations": ["cooling foods", "avoid heat", "sweet fruits", "coconut water"],
            "herbs": ["aloe vera", "coriander", "fennel"]
        },
        "fall_winter": {
            "dominant_dosha": "vata",
            "recommendations": ["warm foods", "oil massage", "regular routine", "grounding practices"],
            "herbs": ["ashwagandha", "brahmi", "sesame oil"]
        }
    },
    
    "vedic_astrology": {
        "planetary_influences": {
            "sun": {"dosha": "pitta", "body_parts": ["heart", "eyes"], "qualities": ["leadership", "vitality"]},
            "moon": {"dosha": "kapha", "body_parts": ["mind", "stomach"], "qualities": ["emotions", "nurturing"]},
            "mars": {"dosha": "pitta", "body_parts": ["blood", "muscles"], "qualities": ["energy", "courage"]},
            "mercury": {"dosha": "vata", "body_parts": ["nervous system", "skin"], "qualities": ["communication", "intelligence"]},
            "jupiter": {"dosha": "kapha", "body_parts": ["liver", "fat"], "qualities": ["wisdom", "expansion"]},
            "venus": {"dosha": "kapha", "body_parts": ["reproductive system", "kidneys"], "qualities": ["beauty", "harmony"]},
            "saturn": {"dosha": "vata", "body_parts": ["bones", "joints"], "qualities": ["discipline", "longevity"]}
        }
    }
}

def get_current_season():
    """Determine current season based on date"""
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
    elif def generate_ai_response(query, user_constitution=None, user_age=None, current_season=None, symptoms=None, context=None):
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
        }quest.get_json()
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
                'message': 'Subscribe to access personalized AI guidance from Dr. Helen Thomas DC'
            }), 403
        
        # Get user's constitution if available
        user_constitution = None
        user_age = None
        
        if user_id or email:
            # Find most recent assessment
            assessment_query = Assessment.query
            if user_id:
                assessment_query = assessment_query.filter_by(user_id=user_id)
            elif email:
                assessment_query = assessment_query.filter_by(email=email)
            
            recent_assessment = assessment_query.order_by(Assessment.created_at.desc()).first()
            if recent_assessment:
                user_constitution = recent_assessment.constitution
        
        # Generate AI response
        ai_response = generate_ai_response(
            query=query,
            user_constitution=user_constitution,
            user_age=user_age,
            context=data.get('context', {})
        )
        
        # Log the query (for analytics and improvement)
        # Could store in a QueryLog model for future reference
        
        return jsonify({
            'success': True,
            'query': query,
            'response': ai_response,
            'constitution': user_constitution,
            'personalized': bool(user_constitution),
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_query_bp.route('/subscription/status', methods=['POST'])
def check_subscription():
    """Check subscription status"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        subscription = NewsletterSubscription.query.filter_by(email=email).first()
        
        if not subscription:
            return jsonify({
                'success': True,
                'subscribed': False,
                'active': False,
                'message': 'No subscription found'
            })
        
        return jsonify({
            'success': True,
            'subscribed': True,
            'active': subscription.is_active,
            'subscribed_at': subscription.subscribed_at.isoformat() if subscription.subscribed_at else None,
            'preferences': subscription.get_preferences()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_query_bp.route('/knowledge/constitutions', methods=['GET'])
def get_constitution_info():
    """Get detailed information about all 13 constitutions"""
    try:
        # Extend basic knowledge with the 13 constitution system
        extended_constitutions = dict(AYURVEDIC_KNOWLEDGE["constitutions"])
        
        # Add combination constitutions
        combinations = [
            "vata-pitta", "vata-kapha", "pitta-kapha", "pitta-vata", 
            "kapha-vata", "kapha-pitta", "tri-dosha"
        ]
        
        # Add advanced energetic principles
        advanced_types = {
            "ojas": {
                "description": "Vital essence and immunity strength",
                "signs_balanced": ["radiant health", "strong immunity", "peaceful mind"],
                "signs_imbalanced": ["chronic fatigue", "poor immunity", "dull complexion"],
                "recommendations": ["quality sleep", "fresh foods", "spiritual practice"]
            },
            "tejas": {
                "description": "Inner fire and spiritual insight",
                "signs_balanced": ["sharp mind", "clear vision", "good judgment"],
                "signs_imbalanced": ["mental fog", "poor concentration", "dull perception"],
                "recommendations": ["meditation", "study", "ghee consumption"]
            },
            "prana": {
                "description": "Life energy and consciousness",
                "signs_balanced": ["vibrant energy", "clear breathing", "present awareness"],
                "signs_imbalanced": ["shallow breathing", "low energy", "disconnection"],
                "recommendations": ["pranayama", "fresh air", "mindfulness"]
            }
        }
        
        extended_constitutions.update(advanced_types)
        
        return jsonify({
            'success': True,
            'constitutions': extended_constitutions,
            'total_types': 13,
            'categories': ['primary_doshas', 'dual_constitutions', 'tri_dosha', 'energetic_principles']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_query_bp.route('/guidance/seasonal', methods=['GET'])
def get_seasonal_guidance():
    """Get current seasonal guidance"""
    try:
        current_season = get_current_season()
        season_data = AYURVEDIC_KNOWLEDGE["seasons"].get(current_season, {})
        
        return jsonify({
            'success': True,
            'current_season': current_season,
            'guidance': season_data,
            'general_advice': f"During {current_season}, {season_data.get('dominant_dosha', 'unknown')} dosha tends to increase."
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ai_query_bp.route('/avatar/contextual-script', methods=['POST'])
def get_contextual_avatar_script():
    """Get avatar script based on user context and query"""
    try:
        data = request.get_json()
        context = data.get('context', 'general')
        user_constitution = data.get('constitution')
        current_season = get_current_season()
        
        scripts = {
            'welcome': f"Hello, I'm Dr. Helen Thomas, DC. Welcome to Your Healing Guide powered by NanoSutracore - my advanced AI system integrating Healing Airwaves and Ayurveda Wisdom from 44 years of clinical practice.",
            
            'assessment_intro': "I'm here to guide you through discovering your Ayurvedic constitution using NanoSutracore intelligence. This assessment draws from my Healing Airwaves methodology and traditional Ayurveda Wisdom to reveal your unique body-mind type among the 13 constitutional patterns.",
            
            'seasonal': f"Right now we're in {current_season} season. NanoSutracore analyzes how this affects your dosha balance and provides personalized guidance from my integrated knowledge bases.",
            
            'constitution_result': f"Based on your assessment processed through NanoSutracore, your constitution is {user_constitution}. This is your unique blueprint - my AI system now personalizes all guidance specifically for your type." if user_constitution else "Your constitution is your unique blueprint. NanoSutracore will personalize all guidance once we determine your type.",
            
            'subscription_invite': "To access NanoSutracore's full intelligence - combining Healing Airwaves, Ayurveda Wisdom, and my 44 years of clinical experience - join our healing community. Ask any question about symptoms, nutrition, lifestyle, or Vedic astrology.",
            
            'query_response': "NanoSutracore is processing your question through my integrated knowledge bases - Healing Airwaves methodology and traditional Ayurveda Wisdom - to provide personalized guidance based on your constitution, current season, and clinical protocols I've developed over four decades.",
            
            'nanosutracore_intro': "NanoSutracore is my advanced AI reasoning system that combines three powerful knowledge bases: Healing Airwaves with my specialized clinical protocols, Ayurveda Wisdom from classical texts, and 44 years of practical patient experience. This creates unprecedented personalized guidance."
        }
        
        script = scripts.get(context, scripts['welcome'])
        
        return jsonify({
            'success': True,
            'script': script,
            'context': context,
            'season': current_season,
            'constitution': user_constitution
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
