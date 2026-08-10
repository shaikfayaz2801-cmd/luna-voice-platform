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
