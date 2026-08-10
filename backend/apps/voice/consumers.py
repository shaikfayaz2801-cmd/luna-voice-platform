"""
Full Voice WebSocket Consumer — STT → AI → TTS pipeline with barge-in support.
"""
import asyncio
import json
import logging
import io
from typing import Optional
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.conf import settings

logger = logging.getLogger(__name__)

SILENCE_THRESHOLD_SECONDS = 1.2
AUDIO_CHUNK_SIZE = 4096


class VoiceConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time voice conversations with Luna.

    Protocol (client → server):
      - Binary frames: raw PCM audio chunks (16kHz, mono, 16-bit)
      - Text frame JSON: {"type": "config", "language": "en"} | {"type": "barge_in"}

    Protocol (server → client):
      - Binary frames: MP3/PCM TTS audio chunks
      - Text frame JSON: {"type": "transcript", "text": "..."} | {"type": "status", "state": "listening|processing|speaking"} | {"type": "error", "message": "..."}
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.language = 'en'
        self.audio_buffer: list[bytes] = []
        self.is_speaking = False          # TTS currently playing
        self.is_processing = False        # AI/STT currently running
        self.silence_timer: Optional[asyncio.TimerHandle] = None
        self.conversation_history: list[dict] = []
        self.session_id: Optional[str] = None
        self._speaking_task: Optional[asyncio.Task] = None

    async def connect(self):
        self.user = self.scope.get('user')
        if not self.user or not self.user.is_authenticated:
            await self.close(code=4001)
            return

        await self.accept()
        self.language = getattr(self.user, 'language', 'en')

        # Load system prompt
        self.system_prompt = await self._get_system_prompt()
        self.conversation_history = [{'role': 'system', 'content': self.system_prompt}]

        # Create voice session in DB
        self.session_id = await self._create_voice_session()

        await self._send_status('idle')
        logger.info(f"VoiceConsumer connected: user={self.user.email}")

    async def disconnect(self, close_code):
        self._cancel_silence_timer()
        if self._speaking_task:
            self._speaking_task.cancel()
        if self.session_id:
            await self._close_voice_session(self.session_id)
        logger.info(f"VoiceConsumer disconnected: code={close_code}")

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            await self._handle_control_message(text_data)
        elif bytes_data:
            await self._handle_audio_chunk(bytes_data)

    async def _handle_control_message(self, text_data: str):
        try:
            data = json.loads(text_data)
            msg_type = data.get('type')

            if msg_type == 'config':
                self.language = data.get('language', self.language)
                await self._send_json({'type': 'config_ack', 'language': self.language})

            elif msg_type == 'barge_in':
                await self._handle_barge_in()

            elif msg_type == 'ping':
                await self._send_json({'type': 'pong'})

        except json.JSONDecodeError:
            pass

    async def _handle_barge_in(self):
        """User started speaking while Luna is speaking — interrupt TTS."""
        if self._speaking_task and not self._speaking_task.done():
            self._speaking_task.cancel()
            self._speaking_task = None
        self.is_speaking = False
        self.audio_buffer = []
        await self._send_status('listening')
        logger.debug("Barge-in received — TTS interrupted")

    async def _handle_audio_chunk(self, audio_data: bytes):
        """Buffer incoming PCM audio chunks and detect end-of-speech via silence."""
        if self.is_processing or self.is_speaking:
            return  # Ignore audio during processing/speaking unless barge-in

        self.audio_buffer.append(audio_data)

        # Reset silence timer on each audio chunk
        self._cancel_silence_timer()
        loop = asyncio.get_event_loop()
        self.silence_timer = loop.call_later(
            SILENCE_THRESHOLD_SECONDS,
            lambda: asyncio.ensure_future(self._process_buffered_audio())
        )

        await self._send_status('listening')

    async def _process_buffered_audio(self):
        """Called after silence detected — run STT → AI → TTS pipeline."""
        if not self.audio_buffer:
            return

        audio_bytes = b''.join(self.audio_buffer)
        self.audio_buffer = []
        self.is_processing = True

        await self._send_status('processing')

        try:
            # 1. Speech-to-Text
            transcript = await self._transcribe(audio_bytes)
            if not transcript or not transcript.strip():
                await self._send_status('idle')
                return

            await self._send_json({'type': 'transcript', 'text': transcript, 'speaker': 'user'})
            logger.debug(f"STT result: {transcript[:80]}")

            # 2. AI response
            self.conversation_history.append({'role': 'user', 'content': transcript})
            ai_response = await self._get_ai_response()

            self.conversation_history.append({'role': 'assistant', 'content': ai_response})
            await self._send_json({'type': 'transcript', 'text': ai_response, 'speaker': 'luna'})
            logger.debug(f"AI response: {ai_response[:80]}")

            # 3. Text-to-Speech
            self.is_processing = False
            self.is_speaking = True
            await self._send_status('speaking')
            self._speaking_task = asyncio.ensure_future(self._stream_tts(ai_response))

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.exception(f"Voice pipeline error: {e}")
            await self._send_json({'type': 'error', 'message': 'Voice processing failed.'})
            await self._send_status('idle')
        finally:
            self.is_processing = False

    async def _transcribe(self, audio_bytes: bytes) -> str:
        """Run Speech-to-Text on buffered audio."""
        from apps.voice.providers.openai_stt import OpenAISTTProvider
        from apps.voice.providers.google_stt import GoogleSTTProvider

        provider_name = settings.STT_PROVIDER
        try:
            if provider_name == 'google':
                provider = GoogleSTTProvider()
            else:
                provider = OpenAISTTProvider()

            return await asyncio.get_event_loop().run_in_executor(
                None, provider.transcribe, audio_bytes
            )
        except Exception as e:
            logger.exception(f"STT error: {e}")
            return ""

    async def _get_ai_response(self) -> str:
        """Get complete AI response (non-streaming for voice for lower latency chunking)."""
        from apps.ai.factory import get_ai_provider
        provider = get_ai_provider()
        chunks = []
        async for chunk in provider.complete(self.conversation_history, stream=True):
            chunks.append(chunk)
        return ''.join(chunks)

    async def _stream_tts(self, text: str):
        """Convert text to speech and stream audio bytes to client."""
        from apps.voice.providers.elevenlabs_tts import ElevenLabsTTSProvider
        from apps.voice.providers.google_tts import GoogleTTSProvider

        provider_name = settings.TTS_PROVIDER
        try:
            if provider_name == 'google':
                provider = GoogleTTSProvider()
                audio_bytes = await asyncio.get_event_loop().run_in_executor(
                    None, provider.synthesize, text, self.language
                )
                # Send in chunks
                chunk_size = 4096
                for i in range(0, len(audio_bytes), chunk_size):
                    if self._speaking_task and self._speaking_task.cancelled():
                        break
                    await self.send(bytes_data=audio_bytes[i:i+chunk_size])
                    await asyncio.sleep(0.01)
            else:
                provider = ElevenLabsTTSProvider()
                async for chunk in provider.stream_tts(text):
                    if self._speaking_task and self._speaking_task.cancelled():
                        break
                    await self.send(bytes_data=chunk)
                    await asyncio.sleep(0.005)

        except asyncio.CancelledError:
            logger.debug("TTS stream cancelled (barge-in)")
        except Exception as e:
            logger.exception(f"TTS error: {e}")
        finally:
            self.is_speaking = False
            self._speaking_task = None
            await self._send_status('idle')

    def _cancel_silence_timer(self):
        if self.silence_timer:
            self.silence_timer.cancel()
            self.silence_timer = None

    async def _send_status(self, state: str):
        await self._send_json({'type': 'status', 'state': state})

    async def _send_json(self, data: dict):
        try:
            await self.send(text_data=json.dumps(data))
        except Exception:
            pass

    @database_sync_to_async
    def _get_system_prompt(self) -> str:
        from apps.personality.models import Personality, UserPersonalitySettings
        try:
            settings_obj = UserPersonalitySettings.objects.select_related('personality').get(user=self.user)
            return settings_obj.personality.system_prompt
        except UserPersonalitySettings.DoesNotExist:
            p = Personality.objects.filter(is_default=True).first()
            if p:
                return p.system_prompt
        return (
            "You are Luna, a warm and friendly AI voice companion. Be concise in voice mode — "
            "keep responses under 3 sentences unless the user asks for detail. "
            "You are an AI and are transparent about this. Be warm, empathetic, and helpful."
        )

    @database_sync_to_async
    def _create_voice_session(self) -> str:
        from apps.voice.models import VoiceSession
        session = VoiceSession.objects.create(
            user=self.user,
            provider_stt=settings.STT_PROVIDER,
            provider_tts=settings.TTS_PROVIDER,
        )
        return str(session.id)

    @database_sync_to_async
    def _close_voice_session(self, session_id: str):
        from apps.voice.models import VoiceSession
        from django.utils import timezone
        VoiceSession.objects.filter(id=session_id).update(ended_at=timezone.now())
