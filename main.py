import os
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS
CORS(app)

# Initialize database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    constitution_type = db.Column(db.String(50))
    responses = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class NewsletterSubscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

def get_current_season():
    month = datetime.now().month
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "fall"
    else:
        return "winter"

@app.route('/')
def index():
    return jsonify({
        'status': 'online',
        'service': 'Your Healing Guide API',
        'version': '1.0',
        'endpoints': {
            'health': '/health',
            'ai_query': '/api/ai-query',
            'newsletter': '/api/newsletter/subscribe',
            'lead_magnet': '/api/lead-magnet'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/ai-query', methods=['POST'])
def ai_query():
    try:
        import openai
        
        data = request.json
        user_message = data.get('message', '')
        constitution_type = data.get('constitution_type', 'unknown')
        
        openai_key = os.environ.get('OPENAI_API_KEY')
        if not openai_key:
            return jsonify({'error': 'OpenAI API key not configured'}), 500
        
        client = openai.OpenAI(api_key=openai_key)
        
        system_prompt = f"""You are Dr. Helen Thomas, a Doctor of Chiropractic with 44 years of clinical experience 
and deep expertise in Ayurvedic medicine. You've treated over 15,000 patients.
Current season: {get_current_season()}
User's constitution type: {constitution_type}
Provide warm, knowledgeable guidance combining traditional Ayurvedic wisdom with modern health science."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return jsonify({
            'response': response.choices[0].message.content,
            'season': get_current_season()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/newsletter/subscribe', methods=['POST'])
def newsletter_subscribe():
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        existing = NewsletterSubscription.query.filter_by(email=email).first()
        if existing:
            return jsonify({'message': 'Already subscribed', 'email': email})
        
        subscription = NewsletterSubscription(email=email)
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({'message': 'Successfully subscribed', 'email': email}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/lead-magnet', methods=['GET'])
def get_lead_magnet():
    try:
        pdf_path = os.path.join(os.path.dirname(__file__), 'The_13_Ayurvedic_Body_Types.pdf')
        if os.path.exists(pdf_path):
            return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name='The_13_Ayurvedic_Body_Types.pdf')
        else:
            return jsonify({'error': 'PDF not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.dirname(__file__), 'favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
