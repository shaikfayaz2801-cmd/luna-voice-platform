import os

BASE_DIR = r"c:\expense-gravity\backend"

def write_f(path, content):
    full = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

files = {}

files['apps/chat/models.py'] = r'''
import uuid
from django.db import models
from django.conf import settings

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='conversations')
    title = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.title or 'Chat'}"

class Message(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    tokens_used = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class MessageAttachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='chat_attachments/')
    file_type = models.CharField(max_length=50)
'''

files['apps/chat/serializers.py'] = r'''
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
'''

files['apps/chat/views.py'] = r'''
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from apps.ai.factory import get_ai_provider
import json

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user, is_archived=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation_id=self.kwargs['conversation_id'],
            conversation__user=self.request.user
        ).order_by('created_at')

class StreamingMessageView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        content = request.data.get('content')
        if not content:
            return Response({"error": "Content required"}, status=400)
            
        conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        Message.objects.create(conversation=conversation, role='user', content=content)
        
        provider = get_ai_provider()
        
        async def stream_response():
            messages = [{"role": "system", "content": "You are Luna, a warm AI companion."}]
            for msg in conversation.messages.all().order_by('created_at'):
                messages.append({"role": msg.role, "content": msg.content})
            
            full_response = ""
            async for chunk in provider.complete(messages, stream=True):
                full_response += chunk
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
            
            # Save the complete message sync context is needed here, simplified for streaming
            from asgiref.sync import sync_to_async
            @sync_to_async
            def save_msg():
                Message.objects.create(conversation=conversation, role='assistant', content=full_response)
            await save_msg()
            yield "data: [DONE]\n\n"

        return StreamingHttpResponse(stream_response(), content_type='text/event-stream')
'''

files['apps/chat/urls.py'] = r'''
from django.urls import path
from .views import ConversationListCreateView, ConversationDetailView, MessageListView, StreamingMessageView

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list'),
    path('conversations/<uuid:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<uuid:conversation_id>/messages/', MessageListView.as_view(), name='message-list'),
    path('conversations/<uuid:conversation_id>/stream/', StreamingMessageView.as_view(), name='message-stream'),
]
'''

files['apps/chat/consumers.py'] = r'''
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.ai.factory import get_ai_provider

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        provider = get_ai_provider()
        
        messages = [{"role": "user", "content": message}]
        full_response = ""
        
        async for chunk in provider.complete(messages, stream=True):
            full_response += chunk
            await self.send(text_data=json.dumps({'chunk': chunk}))
        
        await self.send(text_data=json.dumps({'done': True}))
'''

files['apps/chat/routing.py'] = r'''
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<conversation_id>[0-9a-f-]+)/$', consumers.ChatConsumer.as_asgi()),
]
'''

files['apps/chat/tasks.py'] = r'''
from celery import shared_task
@shared_task
def summarize_conversation(conversation_id):
    pass
'''

files['apps/chat/admin.py'] = r'''
from django.contrib import admin
from .models import Conversation, Message
admin.site.register(Conversation)
admin.site.register(Message)
'''

files['apps/chat/tests.py'] = r'''
from django.test import TestCase
class ChatTests(TestCase): pass
'''

files['apps/memory/models.py'] = r'''
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
'''

files['apps/memory/serializers.py'] = r'''
from rest_framework import serializers
from .models import Memory, MemoryTag

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = ['id', 'content', 'memory_type', 'importance', 'created_at', 'metadata']
'''

files['apps/memory/embeddings.py'] = r'''
from apps.ai.factory import get_ai_provider

async def get_embedding(text: str) -> list[float]:
    provider = get_ai_provider()
    return await provider.get_embedding(text)

def get_embedding_sync(text: str) -> list[float]:
    import asyncio
    return asyncio.run(get_embedding(text))
'''

files['apps/memory/retrieval.py'] = r'''
from .models import Memory
from .embeddings import get_embedding_sync

def retrieve_relevant_memories(user_id, query: str, limit: int = 5):
    query_embedding = get_embedding_sync(query)
    # Uses pgvector cosine distance
    memories = Memory.objects.filter(user_id=user_id).order_by(
        Memory.embedding.cosine_distance(query_embedding)
    )[:limit]
    return list(memories)
'''

files['apps/memory/views.py'] = r'''
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Memory
from .serializers import MemorySerializer
from .retrieval import retrieve_relevant_memories

class MemoryListCreateView(generics.ListCreateAPIView):
    serializer_class = MemorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Memory.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # In a real app, generate embedding here before save
        serializer.save(user=self.request.user)

class MemoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Memory.objects.filter(user=self.request.user)

class MemorySearchView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        query = request.data.get('query')
        limit = int(request.data.get('limit', 5))
        memories = retrieve_relevant_memories(request.user.id, query, limit)
        serializer = MemorySerializer(memories, many=True)
        return Response(serializer.data)
'''

files['apps/memory/urls.py'] = r'''
from django.urls import path
from .views import MemoryListCreateView, MemoryDetailView, MemorySearchView

urlpatterns = [
    path('', MemoryListCreateView.as_view(), name='memory-list'),
    path('<uuid:pk>/', MemoryDetailView.as_view(), name='memory-detail'),
    path('search/', MemorySearchView.as_view(), name='memory-search'),
]
'''
files['apps/memory/admin.py'] = r'''
from django.contrib import admin
from .models import Memory
admin.site.register(Memory)
'''
files['apps/memory/tests.py'] = r'''
from django.test import TestCase
'''

files['apps/ai/providers/base.py'] = r'''
from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseAIProvider(ABC):
    @abstractmethod
    async def complete(self, messages: list[dict], stream: bool = True) -> AsyncGenerator[str, None]:
        pass
        
    @abstractmethod
    async def get_embedding(self, text: str) -> list[float]:
        pass
'''

files['apps/ai/providers/openai_provider.py'] = r'''
import os
from typing import AsyncGenerator
from openai import AsyncOpenAI
from .base import BaseAIProvider

class OpenAIProvider(BaseAIProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4o"
        self.embedding_model = "text-embedding-3-small"

    async def complete(self, messages: list[dict], stream: bool = True) -> AsyncGenerator[str, None]:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=stream
        )
        if stream:
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        else:
            yield response.choices[0].message.content

    async def get_embedding(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
'''

files['apps/ai/providers/gemini_provider.py'] = r'''
import os
import google.generativeai as genai
from typing import AsyncGenerator
from .base import BaseAIProvider

class GeminiProvider(BaseAIProvider):
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-pro')

    async def complete(self, messages: list[dict], stream: bool = True) -> AsyncGenerator[str, None]:
        # Convert standard messages to Gemini format
        prompt = "\n".join([m['content'] for m in messages])
        response = await self.model.generate_content_async(prompt, stream=stream)
        if stream:
            async for chunk in response:
                yield chunk.text
        else:
            yield response.text

    async def get_embedding(self, text: str) -> list[float]:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return result['embedding']
'''

files['apps/ai/factory.py'] = r'''
from django.conf import settings
from .providers.base import BaseAIProvider
from .providers.openai_provider import OpenAIProvider
from .providers.gemini_provider import GeminiProvider

def get_ai_provider() -> BaseAIProvider:
    provider = getattr(settings, 'AI_PROVIDER', 'openai')
    if provider == 'openai':
        return OpenAIProvider()
    elif provider == 'gemini':
        return GeminiProvider()
    return OpenAIProvider()
'''
files['apps/ai/__init__.py'] = r''''''
files['apps/ai/providers/__init__.py'] = r''''''


for p, c in files.items(): write_f(p, c)
print("Part 2 written successfully.")
