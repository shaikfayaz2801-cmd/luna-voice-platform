from rest_framework import serializers
from .models import VoiceSession, VoiceSettings

class VoiceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoiceSettings
        fields = '__all__'
