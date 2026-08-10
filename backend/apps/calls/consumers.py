"""
Twilio Media Stream WebSocket Consumer for phone call AI conversations.
"""
import asyncio
import base64
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings

logger = logging.getLogger(__name__)

MULAW_SAMPLE_RATE = 8000


class TwilioMediaStreamConsumer(AsyncWebsocketConsumer):
    """
    Handles Twilio Media Stream WebSocket for live phone call AI conversations.
    
    Twilio sends audio in μ-law 8kHz format via binary WebSocket messages.
    We transcribe with STT, get AI response, convert back to μ-law for Twilio.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_sid: str = ''
        self.stream_sid: str = ''
        self.audio_buffer: list[bytes] = []
        self.conversation_history: list[dict] = []
        self.is_processing = False
        self.silence_timer = None

    async def connect(self):
        self.call_sid = self.scope['url_route']['kwargs'].get('call_sid', '')
        await self.accept()
        logger.info(f"Twilio stream connected: call_sid={self.call_sid}")

        # Initialize conversation with Luna system prompt
        self.conversation_history = [{
            'role': 'system',
            'content': (
                "You are Luna, a warm and friendly AI companion on a phone call. "
                "Keep responses SHORT — 1-2 sentences max for phone calls. "
                "Speak naturally as if in a real phone conversation. "
                "You are an AI and are always transparent about this."
            )
        }]

    async def disconnect(self, close_code):
        self._cancel_silence_timer()
        await self._update_call_status('completed')
        logger.info(f"Twilio stream disconnected: call_sid={self.call_sid}")

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        try:
            data = json.loads(text_data)
            event = data.get('event')

            if event == 'connected':
                logger.info(f"Twilio stream event: connected")

            elif event == 'start':
                self.stream_sid = data.get('streamSid', '')
                logger.info(f"Twilio stream started: sid={self.stream_sid}")
                # Send initial greeting
                await self._send_tts_to_twilio(
                    "Hello! This is Luna. How can I help you today?"
                )

            elif event == 'media':
                # Incoming audio chunk (μ-law base64 encoded)
                payload = data.get('media', {}).get('payload', '')
                if payload:
                    audio_bytes = base64.b64decode(payload)
                    await self._handle_audio_chunk(audio_bytes)

            elif event == 'stop':
                logger.info(f"Twilio stream stopped")

        except (json.JSONDecodeError, Exception) as e:
            logger.exception(f"Twilio consumer error: {e}")

    async def _handle_audio_chunk(self, mulaw_bytes: bytes):
        if self.is_processing:
            return

        self.audio_buffer.append(mulaw_bytes)
        self._cancel_silence_timer()

        loop = asyncio.get_event_loop()
        self.silence_timer = loop.call_later(
            1.5,
            lambda: asyncio.ensure_future(self._process_call_audio())
        )

    async def _process_call_audio(self):
        if not self.audio_buffer or self.is_processing:
            return

        audio_data = b''.join(self.audio_buffer)
        self.audio_buffer = []
        self.is_processing = True

        try:
            # Convert μ-law to PCM for STT
            pcm_audio = self._mulaw_to_pcm(audio_data)

            # STT
            from apps.voice.providers.openai_stt import OpenAISTTProvider
            provider = OpenAISTTProvider()
            transcript = await asyncio.get_event_loop().run_in_executor(
                None, provider.transcribe, pcm_audio
            )

            if not transcript or len(transcript.strip()) < 2:
                return

            logger.info(f"Call STT: {transcript[:60]}")
            await self._save_call_log('user', transcript)

            # AI response
            self.conversation_history.append({'role': 'user', 'content': transcript})
            from apps.ai.factory import get_ai_provider
            ai_provider = get_ai_provider()
            chunks = []
            async for chunk in ai_provider.complete(self.conversation_history, stream=True):
                chunks.append(chunk)
            response = ''.join(chunks)

            self.conversation_history.append({'role': 'assistant', 'content': response})
            logger.info(f"Call AI: {response[:60]}")
            await self._save_call_log('ai', response)

            # TTS and send back
            await self._send_tts_to_twilio(response)

        except Exception as e:
            logger.exception(f"Call audio processing error: {e}")
        finally:
            self.is_processing = False

    async def _send_tts_to_twilio(self, text: str):
        """Convert text to μ-law audio and send back through Twilio stream."""
        try:
            from apps.voice.providers.elevenlabs_tts import ElevenLabsTTSProvider
            tts = ElevenLabsTTSProvider()
            mp3_bytes = await asyncio.get_event_loop().run_in_executor(
                None, tts.synthesize_sync, text
            )

            # Convert MP3 to μ-law 8kHz for Twilio
            mulaw_audio = self._mp3_to_mulaw(mp3_bytes)
            if not mulaw_audio:
                return

            # Chunk and send in Twilio Media format
            chunk_size = 160  # 20ms at 8kHz
            for i in range(0, len(mulaw_audio), chunk_size):
                chunk = mulaw_audio[i:i + chunk_size]
                encoded = base64.b64encode(chunk).decode('utf-8')
                message = json.dumps({
                    'event': 'media',
                    'streamSid': self.stream_sid,
                    'media': {'payload': encoded}
                })
                await self.send(text_data=message)
                await asyncio.sleep(0.018)  # ~20ms pacing

        except Exception as e:
            logger.exception(f"TTS-to-Twilio error: {e}")

    def _mulaw_to_pcm(self, mulaw_bytes: bytes) -> bytes:
        """Convert μ-law to 16-bit PCM."""
        try:
            import audioop
            return audioop.ulaw2lin(mulaw_bytes, 2)
        except Exception:
            return mulaw_bytes

    def _mp3_to_mulaw(self, mp3_bytes: bytes) -> bytes:
        """Convert MP3 audio to μ-law 8kHz for Twilio."""
        try:
            import io
            from pydub import AudioSegment
            import audioop

            audio = AudioSegment.from_mp3(io.BytesIO(mp3_bytes))
            audio = audio.set_frame_rate(8000).set_channels(1).set_sample_width(2)
            pcm = audio.raw_data
            return audioop.lin2ulaw(pcm, 2)
        except Exception as e:
            logger.warning(f"Audio conversion failed: {e}")
            return b''

    def _cancel_silence_timer(self):
        if self.silence_timer:
            self.silence_timer.cancel()
            self.silence_timer = None

    @database_sync_to_async
    def _update_call_status(self, status: str):
        from apps.calls.models import Call
        from django.utils import timezone
        Call.objects.filter(call_sid=self.call_sid).update(
            status=status,
            ended_at=timezone.now()
        )

    @database_sync_to_async
    def _save_call_log(self, speaker: str, text: str):
        from apps.calls.models import Call, CallLog
        from django.utils import timezone
        try:
            call = Call.objects.get(call_sid=self.call_sid)
            CallLog.objects.create(call=call, speaker=speaker, text=text, timestamp=timezone.now())
        except Call.DoesNotExist:
            pass
