from rest_framework import serializers
from .models import Memory, MemoryTag

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'content', 'memory_type', 'importance', 'created_at', 'metadata']
