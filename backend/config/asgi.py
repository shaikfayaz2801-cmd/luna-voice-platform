import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chat.routing import websocket_urlpatterns as chat_urls
from apps.voice.routing import websocket_urlpatterns as voice_urls
from apps.calls.routing import websocket_urlpatterns as calls_urls

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat_urls + voice_urls + calls_urls
        )
    ),
})
