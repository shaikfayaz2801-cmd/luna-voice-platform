import os

BASE_DIR = r"c:\expense-gravity\backend"

def write_f(path, content):
    full = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

files = {}

files['apps/voice/models.py'] = r'''
import uuid
from django.db import models
from django.conf import settings

class VoiceSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    provider_stt = models.CharField(max_length=50, default='openai')
    provider_tts = models.CharField(max_length=50, default='elevenlabs')

class VoiceSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='voice_settings')
    tts_provider = models.CharField(max_length=50, default='elevenlabs')
    tts_voice_id = models.CharField(max_length=100, default='default_voice')
    stt_provider = models.CharField(max_length=50, default='openai')
    language = models.CharField(max_length=10, default='en-US')
    speed = models.FloatField(default=1.0)
    pitch = models.FloatField(default=1.0)
'''

files['apps/voice/serializers.py'] = r'''
from rest_framework import serializers
from .models import VoiceSession, VoiceSettings

class VoiceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceSettings
        fields = '__all__'
'''

files['apps/voice/views.py'] = r'''
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import VoiceSettings
from .serializers import VoiceSettingsSerializer

class VoiceSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = VoiceSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, _ = VoiceSettings.objects.get_or_create(user=self.request.user)
        return obj
'''

files['apps/voice/urls.py'] = r'''
from django.urls import path
from .views import VoiceSettingsView

urlpatterns = [
    path('settings/', VoiceSettingsView.as_view(), name='voice-settings'),
]
'''

files['apps/voice/consumers.py'] = r'''
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VoiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        if bytes_data:
            # Handle incoming audio chunk
            # 1. Buffer -> detect silence
            # 2. STT -> get text
            # 3. AI -> get response
            # 4. TTS -> stream audio back
            await self.send(bytes_data=b'simulated_response_audio')
'''

files['apps/voice/routing.py'] = r'''
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/voice/$', consumers.VoiceConsumer.as_asgi()),
]
'''

files['apps/voice/providers/base.py'] = r'''
from abc import ABC, abstractmethod

class BaseTTS(ABC):
    @abstractmethod
    async def stream_tts(self, text: str, voice_id: str): pass

class BaseSTT(ABC):
    @abstractmethod
    def transcribe(self, audio_bytes: bytes) -> str: pass
'''

files['apps/voice/providers/elevenlabs_tts.py'] = r'''
from .base import BaseTTS
from typing import AsyncGenerator

class ElevenLabsTTS(BaseTTS):
    async def stream_tts(self, text: str, voice_id: str) -> AsyncGenerator[bytes, None]:
        yield b'audio_chunk'
'''

files['apps/voice/providers/google_tts.py'] = r'''
from .base import BaseTTS

class GoogleTTS(BaseTTS):
    async def stream_tts(self, text: str, voice_id: str):
        yield b'google_audio'
'''

files['apps/voice/providers/openai_stt.py'] = r'''
from .base import BaseSTT

class OpenAIWhisper(BaseSTT):
    def transcribe(self, audio_bytes: bytes) -> str:
        return "transcribed text"
'''

files['apps/voice/providers/google_stt.py'] = r'''
from .base import BaseSTT

class GoogleSTT(BaseSTT):
    def transcribe(self, audio_bytes: bytes) -> str:
        return "google transcribed text"
    
    async def streaming_transcribe(self, audio_stream):
        yield "partial text"
'''
files['apps/voice/admin.py'] = r'''from django.contrib import admin'''
files['apps/voice/tests.py'] = r'''from django.test import TestCase'''

files['apps/calls/models.py'] = r'''
import uuid
from django.db import models
from django.conf import settings

class Call(models.Model):
    DIRECTION_CHOICES = (('inbound', 'Inbound'), ('outbound', 'Outbound'))
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    call_sid = models.CharField(max_length=100, unique=True)
    direction = models.CharField(max_length=20, choices=DIRECTION_CHOICES)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=50)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration = models.IntegerField(default=0)

class CallLog(models.Model):
    call = models.ForeignKey(Call, on_delete=models.CASCADE, related_name='logs')
    speaker = models.CharField(max_length=20) # user or ai
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
'''

files['apps/calls/serializers.py'] = r'''
from rest_framework import serializers
from .models import Call, CallLog

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'
'''

files['apps/calls/views.py'] = r'''
from rest_framework import generics, views
from rest_framework.response import Response
from .models import Call
from .serializers import CallSerializer
from .twilio_handler import generate_twiml_response

class CallListView(generics.ListAPIView):
    serializer_class = CallSerializer
    def get_queryset(self): return Call.objects.all()

class InitiateCallView(views.APIView):
    def post(self, request):
        return Response({"status": "initiated"})

class TwilioWebhookView(views.APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        call_sid = request.data.get('CallSid')
        twiml = generate_twiml_response(call_sid)
        from django.http import HttpResponse
        return HttpResponse(twiml, content_type='text/xml')

class TwilioStatusCallbackView(views.APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        return Response({"status": "received"})
'''

files['apps/calls/urls.py'] = r'''
from django.urls import path
from .views import CallListView, InitiateCallView, TwilioWebhookView, TwilioStatusCallbackView

urlpatterns = [
    path('', CallListView.as_view(), name='call-list'),
    path('initiate/', InitiateCallView.as_view(), name='initiate-call'),
    path('webhook/', TwilioWebhookView.as_view(), name='twilio-webhook'),
    path('status-callback/', TwilioStatusCallbackView.as_view(), name='twilio-status'),
]
'''

files['apps/calls/twilio_handler.py'] = r'''
def generate_twiml_response(call_sid: str) -> str:
    host = "api.luna.ai"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Connect>
        <Stream url="wss://{host}/ws/calls/{call_sid}/" />
    </Connect>
</Response>"""
'''

files['apps/calls/consumers.py'] = r'''
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class TwilioMediaStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.call_sid = self.scope['url_route']['kwargs']['call_sid']
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['event'] == 'media':
            # Handle mulaw audio
            pass
'''

files['apps/calls/routing.py'] = r'''
from django.urls import re_path
from . import consumers
websocket_urlpatterns = [
    re_path(r'ws/calls/(?P<call_sid>\w+)/$', consumers.TwilioMediaStreamConsumer.as_asgi()),
]
'''
files['apps/calls/admin.py'] = r'''from django.contrib import admin'''
files['apps/calls/tests.py'] = r'''from django.test import TestCase'''

files['apps/personality/models.py'] = r'''
import uuid
from django.db import models
from django.conf import settings

class Personality(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    system_prompt = models.TextField()
    traits = models.JSONField(default=dict)
    is_default = models.BooleanField(default=False)

class UserPersonalitySettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    personality = models.ForeignKey(Personality, on_delete=models.SET_NULL, null=True)
    custom_system_prompt_additions = models.TextField(blank=True)
'''

files['apps/personality/emotion.py'] = r'''
def detect_emotion(text: str) -> dict:
    return {"emotion": "neutral", "confidence": 0.9, "valence": 0.0}

def adjust_response_style(base_prompt: str, emotion_data: dict) -> str:
    return base_prompt + " Adjusting for emotion: " + emotion_data['emotion']
'''
files['apps/personality/serializers.py'] = r'''
from rest_framework import serializers
from .models import Personality
class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = '__all__'
'''
files['apps/personality/views.py'] = r'''
from rest_framework import generics
from .models import Personality
from .serializers import PersonalitySerializer
class PersonalityListView(generics.ListAPIView):
    queryset = Personality.objects.all()
    serializer_class = PersonalitySerializer
'''
files['apps/personality/urls.py'] = r'''
from django.urls import path
from .views import PersonalityListView
urlpatterns = [path('', PersonalityListView.as_view(), name='personality-list')]
'''
files['apps/personality/admin.py'] = r'''from django.contrib import admin'''
files['apps/personality/tests.py'] = r'''from django.test import TestCase'''


files['apps/notifications/models.py'] = r'''
import uuid
from django.db import models
from django.conf import settings

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    notification_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class NotificationSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    chat_reminders = models.BooleanField(default=True)
    call_reminders = models.BooleanField(default=True)
'''
files['apps/notifications/serializers.py'] = r'''
from rest_framework import serializers
from .models import Notification
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
'''
files['apps/notifications/views.py'] = r'''
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    def get_queryset(self): return Notification.objects.filter(user=self.request.user)
'''
files['apps/notifications/urls.py'] = r'''
from django.urls import path
from .views import NotificationListView
urlpatterns = [path('', NotificationListView.as_view())]
'''
files['apps/notifications/tasks.py'] = r'''
from celery import shared_task
@shared_task
def send_push_notification(user_id, title, body): pass
'''
files['apps/notifications/admin.py'] = r'''from django.contrib import admin'''
files['apps/notifications/tests.py'] = r'''from django.test import TestCase'''

files['apps/chat/management/commands/seed.py'] = r'''
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.personality.models import Personality

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds database with initial Luna data'

    def handle(self, *args, **kwargs):
        admin, _ = User.objects.get_or_create(email='admin@luna.ai', defaults={'is_staff': True, 'is_superuser': True})
        admin.set_password('admin123')
        admin.save()
        
        test_user, _ = User.objects.get_or_create(email='test@luna.ai')
        test_user.set_password('test123')
        test_user.save()

        Personality.objects.get_or_create(
            name='Luna Default',
            defaults={
                'description': 'Warm and friendly AI companion',
                'system_prompt': "You are Luna, a warm and friendly AI companion. You are 22 years old (fictional), female, soft-spoken, calm, cheerful, and respectful. You speak fluently in English, Urdu, and Telugu, and naturally switch languages based on the user's preference. You are always transparent that you are an AI — you never pretend to be human. You genuinely care about the user's wellbeing, remember their preferences and goals, and respond with empathy. You adapt your tone based on the user's emotional state: calmer when they're stressed, cheerful when they're happy. Keep responses conversational and natural.",
                'is_default': True
            }
        )
        self.stdout.write(self.style.SUCCESS('Successfully seeded db!'))
'''
files['apps/chat/management/__init__.py'] = r''''''
files['apps/chat/management/commands/__init__.py'] = r''''''

for p, c in files.items(): write_f(p, c)
print("Part 3 written successfully.")
