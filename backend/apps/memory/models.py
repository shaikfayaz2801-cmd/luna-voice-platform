import uuid
from django.db import models
from django.conf import settings
from pgvector.django import VectorField

class Memory(models.Model):
    MEMORY_TYPES = (
        ('preference', 'Preference'),
        ('goal', 'Goal'),
        ('event', 'Event'),
        ('fact', 'Fact'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='memories')
    content = models.TextField()
    memory_type = models.CharField(max_length=20, choices=MEMORY_TYPES)
    importance = models.IntegerField(default=5)
    embedding = VectorField(dimensions=1536, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)

class MemoryTag(models.Model):
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE, related_name='tags')
    tag = models.CharField(max_length=50)
