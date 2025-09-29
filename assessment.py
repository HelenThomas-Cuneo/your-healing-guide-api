from flask import Blueprint, request, jsonify
from src.models.assessment import db, Assessment, LibraryContent, NewsletterSubscription
from datetime import datetime
import json

assessment_bp = Blueprint('assessment', __name__)

# Ayurvedic constitution questions and scoring logic
CONSTITUTION_QUESTIONS = [
    {
        "id": 1,
        "category": "physical",
        "question": "What is your natural body frame?",
        "options": [
            {"text": "Thin, light, small-boned", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Medium build, moderate weight", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Large frame, heavy, well-built", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 2,
        "category": "physical",
        "question": "How is your skin typically?",
        "options": [
            {"text": "Dry, rough, thin, cool", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Warm, oily, prone to irritation", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Thick, moist, cool, smooth", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 3,
        "category": "physical",
        "question": "What is your hair like?",
        "options": [
            {"text": "Dry, brittle, thin", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Fine, oily, early graying/balding", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Thick, lustrous, strong", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 4,
        "category": "digestive",
        "question": "How is your appetite?",
        "options": [
            {"text": "Variable, sometimes forget to eat", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Strong, get irritable when hungry", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Steady, can skip meals easily", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 5,
        "category": "digestive",
        "question": "How is your digestion?",
        "options": [
            {"text": "Irregular, gas, bloating", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Strong, sometimes burning", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Slow, heavy feeling after eating", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 6,
        "category": "mental",
        "question": "How do you handle stress?",
        "options": [
            {"text": "Worry, anxiety, restlessness", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Anger, irritability, impatience", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Withdraw, become sluggish", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 7,
        "category": "mental",
        "question": "What is your memory like?",
        "options": [
            {"text": "Quick to learn, quick to forget", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Sharp, clear, focused", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Slow to learn, but good retention", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 8,
        "category": "sleep",
        "question": "How is your sleep?",
        "options": [
            {"text": "Light, interrupted, trouble falling asleep", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Moderate, wake up refreshed", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Deep, long, hard to wake up", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 9,
        "category": "energy",
        "question": "What is your energy pattern?",
        "options": [
            {"text": "Comes in bursts, then crashes", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Steady, intense, focused", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Steady, enduring, slow to start", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    },
    {
        "id": 10,
        "category": "emotional",
        "question": "What are your emotional tendencies?",
        "options": [
            {"text": "Enthusiastic, changeable, anxious", "vata": 3, "pitta": 0, "kapha": 0},
            {"text": "Passionate, determined, competitive", "vata": 0, "pitta": 3, "kapha": 0},
            {"text": "Calm, steady, compassionate", "vata": 0, "pitta": 0, "kapha": 3}
        ]
    }
]

def calculate_constitution(answers):
    """Calculate constitution based on answers"""
    scores = {"vata": 0, "pitta": 0, "kapha": 0}
    
    for answer in answers:
        question_id = answer.get('question_id')
        option_index = answer.get('option_index')
        
        # Find the question
        question = next((q for q in CONSTITUTION_QUESTIONS if q['id'] == question_id), None)
        if question and 0 <= option_index < len(question['options']):
            option = question['options'][option_index]
            scores['vata'] += option.get('vata', 0)
            scores['pitta'] += option.get('pitta', 0)
            scores['kapha'] += option.get('kapha', 0)
    
    # Determine primary constitution
    primary = max(scores, key=scores.get)
    
    # Check for dual constitution (if two doshas are close)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    secondary = None
    
    if len(sorted_scores) > 1:
        primary_score = sorted_scores[0][1]
        secondary_score = sorted_scores[1][1]
        
        # If secondary is within 20% of primary, it's a dual constitution
        if secondary_score >= primary_score * 0.8:
            secondary = sorted_scores[1][0]
    
    return {
        'primary': primary,
        'secondary': secondary,
        'scores': scores,
        'constitution': f"{primary}-{secondary}" if secondary else primary
    }

def generate_recommendations(constitution_result):
    """Generate personalized recommendations based on constitution"""
    primary = constitution_result['primary']
    secondary = constitution_result['secondary']
    
    recommendations = {
        'diet': [],
        'lifestyle': [],
        'herbs': [],
        'practices': []
    }
    
    # Vata recommendations
    if primary == 'vata' or secondary == 'vata':
        recommendations['diet'].extend([
            "Warm, cooked foods",
            "Sweet, sour, and salty tastes",
            "Regular meal times",
            "Avoid cold, dry, raw foods"
        ])
        recommendations['lifestyle'].extend([
            "Regular daily routine",
            "Adequate rest and sleep",
            "Gentle, grounding exercises",
            "Oil massage (abhyanga)"
        ])
        recommendations['herbs'].extend([
            "Ashwagandha for stress",
            "Triphala for digestion",
            "Brahmi for mental clarity"
        ])
        recommendations['practices'].extend([
            "Meditation and pranayama",
            "Warm oil treatments",
            "Gentle yoga"
        ])
    
    # Pitta recommendations
    if primary == 'pitta' or secondary == 'pitta':
        recommendations['diet'].extend([
            "Cool, fresh foods",
            "Sweet, bitter, and astringent tastes",
            "Avoid spicy, oily, acidic foods",
            "Eat at regular times"
        ])
        recommendations['lifestyle'].extend([
            "Avoid overheating",
            "Moderate exercise",
            "Cool environments",
            "Avoid excessive competition"
        ])
        recommendations['herbs'].extend([
            "Aloe vera for cooling",
            "Neem for purification",
            "Coriander for digestion"
        ])
        recommendations['practices'].extend([
            "Cooling pranayama",
            "Moon gazing",
            "Swimming or water activities"
        ])
    
    # Kapha recommendations
    if primary == 'kapha' or secondary == 'kapha':
        recommendations['diet'].extend([
            "Light, warm, spicy foods",
            "Pungent, bitter, and astringent tastes",
            "Avoid heavy, oily, sweet foods",
            "Eat lighter meals"
        ])
        recommendations['lifestyle'].extend([
            "Regular vigorous exercise",
            "Stay active and stimulated",
            "Avoid excessive sleep",
            "Dry brushing"
        ])
        recommendations['herbs'].extend([
            "Ginger for digestion",
            "Turmeric for inflammation",
            "Trikatu for metabolism"
        ])
        recommendations['practices'].extend([
            "Energizing pranayama",
            "Dynamic yoga",
            "Early morning activities"
        ])
    
    return recommendations

@assessment_bp.route('/questions', methods=['GET'])
def get_questions():
    """Get all assessment questions"""
    return jsonify({
        'success': True,
        'questions': CONSTITUTION_QUESTIONS
    })

@assessment_bp.route('/submit', methods=['POST'])
def submit_assessment():
    """Submit assessment answers and get constitution result"""
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        email = data.get('email')
        user_id = data.get('user_id')
        
        if not answers:
            return jsonify({'success': False, 'error': 'No answers provided'}), 400
        
        # Calculate constitution
        constitution_result = calculate_constitution(answers)
        
        # Generate recommendations
        recommendations = generate_recommendations(constitution_result)
        
        # Save to database
        assessment = Assessment(
            user_id=user_id,
            email=email,
            constitution=constitution_result['constitution'],
            secondary_constitution=constitution_result['secondary']
        )
        
        assessment.set_scores(constitution_result['scores'])
        assessment.set_answers(answers)
        assessment.set_recommendations(recommendations)
        
        db.session.add(assessment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'assessment_id': assessment.id,
            'constitution': constitution_result,
            'recommendations': recommendations
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@assessment_bp.route('/<int:assessment_id>', methods=['GET'])
def get_assessment(assessment_id):
    """Get assessment results by ID"""
    try:
        assessment = Assessment.query.get_or_404(assessment_id)
        return jsonify({
            'success': True,
            'assessment': assessment.to_dict()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@assessment_bp.route('/library', methods=['GET'])
def get_library():
    """Get library content"""
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        
        query = LibraryContent.query.filter_by(is_published=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(LibraryContent.title.contains(search))
        
        content = query.all()
        
        return jsonify({
            'success': True,
            'content': [item.to_dict() for item in content]
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@assessment_bp.route('/newsletter/subscribe', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    try:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        # Check if already subscribed
        existing = NewsletterSubscription.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                return jsonify({'success': False, 'error': 'Already subscribed'}), 400
            else:
                # Reactivate subscription
                existing.is_active = True
                existing.unsubscribed_at = None
                db.session.commit()
                return jsonify({'success': True, 'message': 'Subscription reactivated'})
        
        # Create new subscription
        subscription = NewsletterSubscription(
            email=email,
            name=name
        )
        
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Successfully subscribed to newsletter'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@assessment_bp.route('/avatar/speak', methods=['POST'])
def avatar_speak():
    """Generate avatar speech content"""
    try:
        data = request.get_json()
        script_type = data.get('type', 'welcome')
        context = data.get('context', {})
        
        # Avatar scripts based on type
        scripts = {
            'welcome': "Hello and welcome. I'm Dr. Helen Thomas, DC. I've spent 44 years in the clinic, taught Ayurveda at college, and wrote two books — so you don't have to guess what works.",
            'pulse': "The pulse shows me what's happening right now in your body. It reveals which areas are in balance or out of balance. It tells me if there's dryness, heat, inflammation, or congestion and stagnation.",
            'consultation': "The first step is always simple: remoisturizing dryness, cooling heat and inflammation, or flushing mucus and stagnation. This is the beginning of real healing. Let's begin.",
            'digestive': "If you feel burning, bloating, or reflux, your body is signaling that digestion is out of balance. What to do: sip cumin, coriander, and fennel tea.",
            'sleep': "If you can't fall asleep, wake at night, or feel anxious in the evening, it may be your Vata running too fast. Try warm milk with nutmeg.",
            'energy': "If you feel heavy, sluggish mornings, this may be Kapha energy that needs gentle stirring. Start with ginger-lemon tea and gentle movement."
        }
        
        script = scripts.get(script_type, scripts['welcome'])
        
        return jsonify({
            'success': True,
            'script': script,
            'type': script_type
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
