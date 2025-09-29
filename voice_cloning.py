from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import tempfile
import logging
from ..services.elevenlabs_service import ElevenLabsService, DR_HELEN_VOICE_CONFIG

logger = logging.getLogger(__name__)

voice_cloning_bp = Blueprint('voice_cloning', __name__)
elevenlabs_service = ElevenLabsService()

# Store Dr. Helen's voice ID
DR_HELEN_VOICE_ID = os.getenv('DR_HELEN_VOICE_ID', 'dj4xxt8wpTWpR9yAZcfn')

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a', 'flac'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@voice_cloning_bp.route('/upload-voice-sample', methods=['POST'])
def upload_voice_sample():
    """Upload voice sample for cloning Dr. Helen's voice"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file format. Please use WAV, MP3, M4A, or FLAC'}), 400
        
        # Save the uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)
        
        # Read the file for ElevenLabs upload
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        
        # Create voice clone
        voice_id = elevenlabs_service.create_voice_clone(
            name=DR_HELEN_VOICE_CONFIG["name"],
            description=DR_HELEN_VOICE_CONFIG["description"],
            audio_files=[audio_data]
        )
        
        # Clean up temporary file
        os.remove(file_path)
        os.rmdir(temp_dir)
        
        if voice_id:
            # Update voice settings for optimal quality
            elevenlabs_service.update_voice_settings(
                voice_id,
                stability=DR_HELEN_VOICE_CONFIG["voice_settings"]["stability"],
                similarity_boost=DR_HELEN_VOICE_CONFIG["voice_settings"]["similarity_boost"]
            )
            
            return jsonify({
                'success': True,
                'voice_id': voice_id,
                'message': 'Voice clone created successfully! Dr. Helen\'s voice is now ready.'
            })
        else:
            return jsonify({'error': 'Failed to create voice clone'}), 500
            
    except Exception as e:
        logger.error(f"Error uploading voice sample: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_cloning_bp.route('/generate-speech', methods=['POST'])
def generate_speech():
    """Generate speech using Dr. Helen's cloned voice"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        voice_id = data.get('voice_id', DR_HELEN_VOICE_ID)
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        if not voice_id:
            return jsonify({'error': 'No voice ID available. Please upload voice sample first.'}), 400
        
        # Generate speech
        audio_data = elevenlabs_service.generate_speech(
            text=text,
            voice_id=voice_id,
            model_id=DR_HELEN_VOICE_CONFIG["model_id"]
        )
        
        if audio_data:
            # Save to temporary file and return
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.write(audio_data)
            temp_file.close()
            
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name='dr_helen_speech.mp3',
                mimetype='audio/mpeg'
            )
        else:
            return jsonify({'error': 'Failed to generate speech'}), 500
            
    except Exception as e:
        logger.error(f"Error generating speech: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_cloning_bp.route('/voices', methods=['GET'])
def get_voices():
    """Get all available voices"""
    try:
        voices = elevenlabs_service.get_voices()
        return jsonify(voices)
    except Exception as e:
        logger.error(f"Error fetching voices: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_cloning_bp.route('/voice-settings/<voice_id>', methods=['GET'])
def get_voice_settings(voice_id):
    """Get settings for a specific voice"""
    try:
        settings = elevenlabs_service.get_voice_settings(voice_id)
        return jsonify(settings)
    except Exception as e:
        logger.error(f"Error fetching voice settings: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_cloning_bp.route('/voice-settings/<voice_id>', methods=['POST'])
def update_voice_settings(voice_id):
    """Update settings for a specific voice"""
    try:
        data = request.get_json()
        stability = data.get('stability', 0.5)
        similarity_boost = data.get('similarity_boost', 0.8)
        
        success = elevenlabs_service.update_voice_settings(voice_id, stability, similarity_boost)
        
        if success:
            return jsonify({'success': True, 'message': 'Voice settings updated successfully'})
        else:
            return jsonify({'error': 'Failed to update voice settings'}), 500
            
    except Exception as e:
        logger.error(f"Error updating voice settings: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_cloning_bp.route('/test-voice/<voice_id>', methods=['POST'])
def test_voice(voice_id):
    """Test a voice with sample text"""
    try:
        test_text = "Hello, I'm Dr. Helen Thomas, DC. Welcome to Your Healing Guide, where ancient wisdom meets modern healing."
        
        audio_data = elevenlabs_service.generate_speech(
            text=test_text,
            voice_id=voice_id,
            model_id=DR_HELEN_VOICE_CONFIG["model_id"]
        )
        
        if audio_data:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.write(audio_data)
            temp_file.close()
            
            return send_file(
                temp_file.name,
                as_attachment=True,
                download_name='voice_test.mp3',
                mimetype='audio/mpeg'
            )
        else:
            return jsonify({'error': 'Failed to generate test audio'}), 500
            
    except Exception as e:
        logger.error(f"Error testing voice: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_cloning_bp.route('/user-info', methods=['GET'])
def get_user_info():
    """Get ElevenLabs user subscription info"""
    try:
        user_info = elevenlabs_service.get_user_info()
        return jsonify(user_info)
    except Exception as e:
        logger.error(f"Error fetching user info: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_cloning_bp.route('/setup-status', methods=['GET'])
def get_setup_status():
    """Check if voice cloning is properly set up"""
    try:
        api_key_configured = bool(elevenlabs_service.api_key)
        voice_id_configured = bool(DR_HELEN_VOICE_ID)
        
        status = {
            'api_key_configured': api_key_configured,
            'voice_id_configured': voice_id_configured,
            'ready': api_key_configured and voice_id_configured
        }
        
        if api_key_configured:
            # Test API connection
            try:
                user_info = elevenlabs_service.get_user_info()
                status['api_connection'] = bool(user_info)
                status['subscription_tier'] = user_info.get('subscription', {}).get('tier', 'unknown')
                status['character_count'] = user_info.get('subscription', {}).get('character_count', 0)
                status['character_limit'] = user_info.get('subscription', {}).get('character_limit', 0)
            except:
                status['api_connection'] = False
        
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error checking setup status: {e}")
        return jsonify({'error': 'Internal server error'}), 500
