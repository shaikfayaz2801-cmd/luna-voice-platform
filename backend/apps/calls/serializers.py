from rest_framework import serializers
from .models import Call, CallLog

class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'
