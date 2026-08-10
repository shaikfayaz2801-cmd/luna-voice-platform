"""
JWT Authentication Middleware for Django Channels WebSocket connections.
Authenticates WebSocket connections via JWT token in query string.
"""
import logging
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that takes a JWT token from the WebSocket query string
    and authenticates the user.
    Usage: ws://localhost:8000/ws/chat/?token=<jwt_access_token>
    """

    async def __call__(self, scope, receive, send):
        close_old_connections()

        try:
            token = self._get_token(scope)
            if token:
                scope['user'] = await self._get_user(token)
            else:
                scope['user'] = AnonymousUser()
        except Exception as e:
            logger.warning(f"WebSocket JWT auth error: {e}")
            scope['user'] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @staticmethod
    def _get_token(scope):
        query_string = scope.get('query_string', b'').decode('utf-8')
        params = parse_qs(query_string)
        token_list = params.get('token', [])
        return token_list[0] if token_list else None

    @staticmethod
    async def _get_user(token_key):
        from channels.db import database_sync_to_async

        @database_sync_to_async
        def get_user_from_token(token):
            try:
                UntypedToken(token)
                decoded = jwt_decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256'],
                )
                user_id = decoded.get('user_id')
                return User.objects.get(id=user_id, is_active=True)
            except (InvalidToken, TokenError, User.DoesNotExist) as e:
                logger.debug(f"Token validation failed: {e}")
                return AnonymousUser()

        return await get_user_from_token(token_key)


def JWTAuthMiddlewareStack(inner):
    """Convenience wrapper combining JWT auth with standard auth stack."""
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
