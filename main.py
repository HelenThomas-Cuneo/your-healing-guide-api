import os
from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'asdf#FGSgvasgf$5$WGT')
CORS(app)

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
        'version': '1.0'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

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
        
        system_prompt = f"""You are Dr. Helen Thomas, a Doctor of Chiropractic with 44 years of clinical experience and deep expertise in Ayurvedic medicine. You've treated over 15,000 patients.
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
```

---

**Commit it, wait for deployment, then test:**
```
https://your-healing-guide-api.vercel.app
