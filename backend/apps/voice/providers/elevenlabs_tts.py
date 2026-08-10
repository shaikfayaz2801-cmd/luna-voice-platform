"""
ElevenLabs TTS Provider — streaming text-to-speech with Luna's voice.
"""
import logging
from typing import AsyncGenerator, Generator
from django.conf import settings

logger = logging.getLogger(__name__)


class ElevenLabsTTSProvider:
    """
    Streams audio from ElevenLabs for Luna's synthetic voice.
    Default voice: configured via ELEVENLABS_VOICE_ID (a warm female voice).
    """

    def __init__(self):
        self.api_key = settings.ELEVENLABS_API_KEY
        self.voice_id = settings.ELEVENLABS_VOICE_ID
        self.model_id = 'eleven_turbo_v2_5'  # Low-latency streaming model

    async def stream_tts(self, text: str, voice_id: str = None) -> AsyncGenerator[bytes, None]:
        """Async generator that yields MP3 audio chunks from ElevenLabs streaming API."""
        import httpx

        vid = voice_id or self.voice_id
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}/stream"

        headers = {
            'xi-api-key': self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'audio/mpeg',
        }
        payload = {
            'text': text,
            'model_id': self.model_id,
            'voice_settings': {
                'stability': 0.65,
                'similarity_boost': 0.80,
                'style': 0.2,
                'use_speaker_boost': True,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                async with client.stream('POST', url, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes(chunk_size=4096):
                        if chunk:
                            yield chunk
        except Exception as e:
            logger.exception(f"ElevenLabs TTS error: {e}")

    def synthesize_sync(self, text: str, voice_id: str = None) -> bytes:
        """Synchronous version for non-async contexts."""
        import requests
        vid = voice_id or self.voice_id
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{vid}"
        headers = {
            'xi-api-key': self.api_key,
            'Content-Type': 'application/json',
        }
        payload = {
            'text': text,
            'model_id': self.model_id,
            'voice_settings': {'stability': 0.65, 'similarity_boost': 0.80},
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            return resp.content
        except Exception as e:
            logger.exception(f"ElevenLabs TTS sync error: {e}")
            return b''
