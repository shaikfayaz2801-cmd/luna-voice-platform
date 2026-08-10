"""
Chat views with full SSE streaming, personality, memory context.
"""
import json
import asyncio
import logging
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from apps.ai.factory import get_ai_provider
from apps.personality.models import Personality, UserPersonalitySettings
from apps.memory.retrieval import retrieve_relevant_memories_sync
from apps.personality.emotion import detect_emotion

logger = logging.getLogger(__name__)


def build_system_prompt(user, conversation) -> str:
    """Build a complete Luna system prompt with personality and memory context."""
    # Get user's personality setting
    try:
        personality_settings = UserPersonalitySettings.objects.get(user=user)
        personality = personality_settings.personality
        custom_additions = personality_settings.custom_system_prompt_additions or ""
    except UserPersonalitySettings.DoesNotExist:
        personality = Personality.objects.filter(is_default=True).first()
        custom_additions = ""

    if personality:
        base_prompt = personality.system_prompt
    else:
        base_prompt = (
            "You are Luna, a warm and friendly AI companion. You are 22 years old (fictional), "
            "female, soft-spoken, calm, cheerful, and respectful. You speak fluently in English, "
            "Urdu, and Telugu, and naturally switch languages based on the user's preference. "
            "You are always transparent that you are an AI — you never pretend to be human. "
            "You genuinely care about the user's wellbeing and respond with empathy."
        )

    # Language instruction
    lang_map = {'en': 'English', 'ur': 'Urdu', 'te': 'Telugu'}
    lang_name = lang_map.get(user.language, 'English')
    lang_instruction = f"\n\nRespond primarily in {lang_name} unless the user writes in a different language."

    # Memory context
    memory_context = ""
    try:
        memories = retrieve_relevant_memories_sync(user.id, conversation.title or "recent conversation")
        if memories:
            memory_lines = "\n".join(f"- {m.content}" for m in memories[:5])
            memory_context = f"\n\nRelevant things you remember about the user:\n{memory_lines}"
    except Exception as e:
        logger.warning(f"Memory retrieval failed: {e}")

    # Custom additions
    additions = f"\n\n{custom_additions}" if custom_additions else ""

    return base_prompt + lang_instruction + memory_context + additions


class ConversationListCreateView(generics.ListCreateAPIView):
    """List all user conversations or create a new one."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Conversation.objects.filter(user=self.request.user)
        archived = self.request.query_params.get('archived', 'false')
        if archived.lower() == 'true':
            return qs.filter(is_archived=True).order_by('-updated_at')
        return qs.filter(is_archived=False).order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConversationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a conversation."""
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)


class MessageListView(generics.ListAPIView):
    """List all messages in a conversation."""
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            conversation_id=self.kwargs['conversation_id'],
            conversation__user=self.request.user
        ).order_by('created_at').select_related('conversation')


class StreamingMessageView(views.APIView):
    """
    POST a user message and stream back Luna's response via SSE.
    SSE format: data: {"chunk": "...", "done": false}\n\n
    Final event: data: {"chunk": "", "done": true, "message_id": "..."}\n\n
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        content = request.data.get('content', '').strip()
        if not content:
            return Response({'error': 'Message content is required.'}, status=status.HTTP_400_BAD_REQUEST)

        conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user
        )

        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            role='user',
            content=content,
        )

        # Auto-title the conversation if it's the first message
        if not conversation.title:
            conversation.title = content[:60] + ('...' if len(content) > 60 else '')
            conversation.save(update_fields=['title'])

        # Detect emotion to adapt response style
        try:
            emotion_data = detect_emotion(content)
        except Exception:
            emotion_data = {}

        system_prompt = build_system_prompt(request.user, conversation)

        # Build message history for AI
        history_messages = list(
            conversation.messages.exclude(id=user_message.id)
            .order_by('created_at')
            .values('role', 'content')
        )[-30:]  # limit context window

        ai_messages = [{'role': 'system', 'content': system_prompt}]
        for msg in history_messages:
            role = msg['role'] if msg['role'] != 'assistant' else 'assistant'
            ai_messages.append({'role': role, 'content': msg['content']})
        ai_messages.append({'role': 'user', 'content': content})

        def sse_generator():
            import asyncio
            provider = get_ai_provider()
            full_response = []

            async def run_stream():
                async for chunk in provider.complete(ai_messages, stream=True):
                    full_response.append(chunk)
                    yield chunk

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                async def collect():
                    async for chunk in run_stream():
                        data = json.dumps({'chunk': chunk, 'done': False})
                        yield f"data: {data}\n\n"

                gen = collect()
                while True:
                    try:
                        chunk_data = loop.run_until_complete(gen.__anext__())
                        yield chunk_data
                    except StopAsyncIteration:
                        break
            finally:
                # Save full AI response
                complete_text = ''.join(full_response)
                if complete_text:
                    ai_msg = Message.objects.create(
                        conversation=conversation,
                        role='assistant',
                        content=complete_text,
                    )
                    conversation.save(update_fields=['updated_at'])
                    yield f"data: {json.dumps({'chunk': '', 'done': True, 'message_id': str(ai_msg.id)})}\n\n"
                loop.close()

        response = StreamingHttpResponse(
            sse_generator(),
            content_type='text/event-stream',
        )
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        return response


class ArchiveConversationView(views.APIView):
    """Toggle archive state of a conversation."""
    permission_classes = [IsAuthenticated]

    def post(self, request, conversation_id):
        conversation = get_object_or_404(
            Conversation, id=conversation_id, user=request.user
        )
        conversation.is_archived = not conversation.is_archived
        conversation.save(update_fields=['is_archived'])
        return Response({'is_archived': conversation.is_archived})


class ConversationStatsView(views.APIView):
    """Return aggregated stats for the authenticated user's conversations."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.db.models import Count, Sum
        stats = Conversation.objects.filter(user=request.user).aggregate(
            total_conversations=Count('id'),
            total_messages=Count('messages'),
        )
        return Response(stats)
