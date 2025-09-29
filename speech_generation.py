from flask import Blueprint, request, jsonify, Response
import os
import requests
from dotenv import load_dotenv

load_dotenv()

speech_generation_bp = Blueprint('speech_generation', __name__)

ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY', 'sk_5187fe66a968b74029c2a3fc057ad2b07def51b48fc60239')
DR_HELEN_VOICE_ID = os.getenv('DR_HELEN_VOICE_ID', 'dj4xxt8wpTWpR9yAZcfn')

@speech_generation_bp.route('/generate-speech', methods=['POST'])
def generate_speech():
    """Generate speech using Dr. Helen's ElevenLabs voice clone"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice_id = data.get('voice_id', DR_HELEN_VOICE_ID)
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
            
        if not ELEVENLABS_API_KEY:
            return jsonify({'error': 'ElevenLabs API key not configured'}), 500
        
        # ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        # Voice settings optimized for Dr. Helen's healing voice
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.75,        # Stable, consistent voice
                "similarity_boost": 0.85, # High similarity to original
                "style": 0.2,            # Subtle style variation
                "use_speaker_boost": True # Enhanced clarity
            }
        }
        
        # Make request to ElevenLabs
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            # Return audio data
            return Response(
                response.content,
                mimetype="audio/mpeg",
                headers={
                    "Content-Disposition": "inline; filename=dr_helen_speech.mp3"
                }
            )
        else:
            error_msg = f"ElevenLabs API error: {response.status_code}"
            if response.text:
                error_msg += f" - {response.text}"
            return jsonify({'error': error_msg}), response.status_code
            
    except Exception as e:
        return jsonify({'error': f'Speech generation failed: {str(e)}'}), 500

@speech_generation_bp.route('/test-voice', methods=['POST'])
def test_voice():
    """Test Dr. Helen's voice with a sample phrase"""
    test_text = "Hello, I'm Dr. Helen Thomas, DC. Welcome to Your Healing Guide, where ancient wisdom meets modern healing."
    
    try:
        # Use the same generation logic
        if not ELEVENLABS_API_KEY:
            return jsonify({'error': 'ElevenLabs API key not configured'}), 500
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{DR_HELEN_VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        payload = {
            "text": test_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.85,
                "style": 0.2,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            return Response(
                response.content,
                mimetype="audio/mpeg",
                headers={
                    "Content-Disposition": "inline; filename=dr_helen_test.mp3"
                }
            )
        else:
            return jsonify({'error': f'Voice test failed: {response.status_code}'}), response.status_code
            
    except Exception as e:
        return jsonify({'error': f'Voice test failed: {str(e)}'}), 500

@speech_generation_bp.route('/voice-status', methods=['GET'])
def voice_status():
    """Check the status of Dr. Helen's voice configuration"""
    return jsonify({
        'api_configured': bool(ELEVENLABS_API_KEY),
        'voice_id': DR_HELEN_VOICE_ID,
        'voice_name': 'Dr. Helen Thomas DC',
        'status': 'ready' if ELEVENLABS_API_KEY else 'api_key_missing'
    })
