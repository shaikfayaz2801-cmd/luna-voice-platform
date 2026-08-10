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
