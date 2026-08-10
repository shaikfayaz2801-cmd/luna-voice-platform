"""
Google Cloud TTS Provider — high-quality neural voices.
"""
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)

VOICE_MAP = {
    'en': ('en-US', 'en-US-Neural2-F'),   # Female neural English
    'ur': ('ur-PK', 'ur-PK-Standard-A'), # Urdu female
    'te': ('te-IN', 'te-IN-Standard-A'), # Telugu female
}


class GoogleTTSProvider:
    """Text-to-speech via Google Cloud TTS."""

    def __init__(self):
        from google.cloud import texttospeech
        creds_json = settings.GOOGLE_TTS_CREDENTIALS
        if creds_json:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(creds_json)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
        self.client = texttospeech.TextToSpeechClient()
        self.texttospeech = texttospeech

    def synthesize(self, text: str, language: str = 'en') -> bytes:
        """Synthesize speech and return MP3 bytes."""
        lang_code, voice_name = VOICE_MAP.get(language, VOICE_MAP['en'])
        try:
            synthesis_input = self.texttospeech.SynthesisInput(text=text)
            voice = self.texttospeech.VoiceSelectionParams(
                language_code=lang_code,
                name=voice_name,
                ssml_gender=self.texttospeech.SsmlVoiceGender.FEMALE,
            )
            audio_config = self.texttospeech.AudioConfig(
                audio_encoding=self.texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,
                pitch=0.0,
            )
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )
            return response.audio_content
        except Exception as e:
            logger.exception(f"Google TTS error: {e}")
            return b''
