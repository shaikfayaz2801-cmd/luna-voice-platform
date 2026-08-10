from rest_framework import serializers
from .models import Conversation, Message, MessageAttachment

class MessageAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachment
        fields = ['id', 'file', 'file_type']

class MessageSerializer(serializers.ModelSerializer):
    attachments = MessageAttachmentSerializer(many=True, read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'role', 'content', 'tokens_used', 'created_at', 'attachments']

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'is_archived']
