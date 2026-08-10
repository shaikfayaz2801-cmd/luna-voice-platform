from rest_framework import generics
from .models import Personality
from .serializers import PersonalitySerializer
class PersonalityListView(generics.ListAPIView):
    queryset = Personality.objects.all()
    serializer_class = PersonalitySerializer
