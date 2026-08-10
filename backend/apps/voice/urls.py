from django.urls import path
from .views import VoiceSettingsView

urlpatterns = [
    path('settings/', VoiceSettingsView.as_view(), name='voice-settings'),
]
