import os
import requests
import json
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ElevenLabsService:
    """Service for integrating with ElevenLabs API for voice synthesis and cloning"""
    
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY', 'sk_5187fe66a968b74029c2a3fc057ad2b07def51b48fc60239')
        self.base_url = "https://api.elevenlabs.io/v1"
        self.headers = {
            "Accept": "application/json",
            "xi-api-key": self.api_key
        }
    
    def get_voices(self) -> Dict[str, Any]:
        """Get all available voices from ElevenLabs"""
        try:
            response = requests.get(
                f"{self.base_url}/voices",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching voices: {e}")
            return {"voices": []}
    
    def create_voice_clone(self, name: str, description: str, audio_files: list) -> Optional[str]:
        """Create a voice clone from audio files"""
        try:
            # Prepare files for upload
            files = []
            for i, audio_file in enumerate(audio_files):
                files.append(('files', (f'sample_{i}.wav', audio_file, 'audio/wav')))
            
            data = {
                'name': name,
                'description': description,
                'labels': json.dumps({"accent": "american", "description": "Dr. Helen Thomas DC", "age": "middle_aged", "gender": "female", "use case": "healing_guide"})
            }
            
            response = requests.post(
                f"{self.base_url}/voices/add",
                headers={"xi-api-key": self.api_key},
                data=data,
                files=files
            )
            response.raise_for_status()
            result = response.json()
            return result.get('voice_id')
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating voice clone: {e}")
            return None
    
    def generate_speech(self, text: str, voice_id: str, model_id: str = "eleven_multilingual_v2") -> Optional[bytes]:
        """Generate speech from text using specified voice"""
        try:
            data = {
                "text": text,
                "model_id": model_id,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.2,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(
                f"{self.base_url}/text-to-speech/{voice_id}",
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating speech: {e}")
            return None
    
    def get_voice_settings(self, voice_id: str) -> Dict[str, Any]:
        """Get voice settings for a specific voice"""
        try:
            response = requests.get(
                f"{self.base_url}/voices/{voice_id}/settings",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching voice settings: {e}")
            return {}
    
    def update_voice_settings(self, voice_id: str, stability: float = 0.5, similarity_boost: float = 0.8) -> bool:
        """Update voice settings for better quality"""
        try:
            data = {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
            
            response = requests.post(
                f"{self.base_url}/voices/{voice_id}/settings/edit",
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error updating voice settings: {e}")
            return False
    
    def delete_voice(self, voice_id: str) -> bool:
        """Delete a custom voice"""
        try:
            response = requests.delete(
                f"{self.base_url}/voices/{voice_id}",
                headers=self.headers
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error deleting voice: {e}")
            return False
    
    def get_user_info(self) -> Dict[str, Any]:
        """Get user subscription info and usage"""
        try:
            response = requests.get(
                f"{self.base_url}/user",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching user info: {e}")
            return {}

# Dr. Helen's voice configuration
DR_HELEN_VOICE_CONFIG = {
    "name": "Dr. Helen Thomas DC",
    "description": "Professional, warm, and authoritative voice of Dr. Helen Thomas DC, with 44 years of clinical experience in Ayurveda and healing.",
    "voice_settings": {
        "stability": 0.6,  # Slightly higher for professional consistency
        "similarity_boost": 0.85,  # High similarity to source voice
        "style": 0.3,  # Moderate style for natural expression
        "use_speaker_boost": True
    },
    "model_id": "eleven_multilingual_v2"  # Best quality model
}
