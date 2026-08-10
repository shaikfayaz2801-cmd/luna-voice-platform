"""
OpenAI STT Provider — Whisper transcription.
"""
import logging
import io
from django.conf import settings

logger = logging.getLogger(__name__)


class OpenAISTTProvider:
    """Transcribes audio using OpenAI Whisper API."""

    def __init__(self):
        import openai
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    def transcribe(self, audio_bytes: bytes, language: str = None) -> str:
        """
        Transcribe audio bytes to text.
        audio_bytes: raw PCM or WebM/Opus audio
        Returns: transcribed string or empty string on failure
        """
        try:
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = 'audio.webm'

            kwargs = {
                'model': 'whisper-1',
                'file': audio_file,
                'response_format': 'text',
            }
            if language:
                kwargs['language'] = language[:2]  # ISO 639-1

            result = self.client.audio.transcriptions.create(**kwargs)
            return result.strip() if isinstance(result, str) else result.text.strip()
        except Exception as e:
            logger.exception(f"OpenAI STT error: {e}")
            return ""
