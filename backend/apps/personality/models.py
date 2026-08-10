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
