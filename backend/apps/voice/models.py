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
