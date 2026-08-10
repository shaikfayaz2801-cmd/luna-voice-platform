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
