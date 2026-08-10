"""
Google Cloud STT Provider — streaming and batch transcription.
"""
import logging
import json
import os
from django.conf import settings

logger = logging.getLogger(__name__)

LANGUAGE_CODE_MAP = {
    'en': 'en-US',
    'ur': 'ur-PK',
    'te': 'te-IN',
}


class GoogleSTTProvider:
    """Transcribes audio using Google Cloud Speech-to-Text."""

    def __init__(self):
        from google.cloud import speech
        creds_json = settings.GOOGLE_STT_CREDENTIALS
        if creds_json:
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                f.write(creds_json)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
        self.client = speech.SpeechClient()

    def transcribe(self, audio_bytes: bytes, language: str = 'en') -> str:
        """Batch transcription of audio bytes."""
        from google.cloud import speech
        try:
            lang_code = LANGUAGE_CODE_MAP.get(language, 'en-US')
            audio = speech.RecognitionAudio(content=audio_bytes)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code=lang_code,
                enable_automatic_punctuation=True,
                model='latest_long',
            )
            response = self.client.recognize(config=config, audio=audio)
            return ' '.join(
                result.alternatives[0].transcript
                for result in response.results
                if result.alternatives
            ).strip()
        except Exception as e:
            logger.exception(f"Google STT error: {e}")
            return ""
