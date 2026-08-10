import os

BASE_DIR = r"c:\expense-gravity\backend"

def write_f(path, content):
    full = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def touch_inits(base):
    for root, dirs, files in os.walk(base):
        if any(d in root for d in ['__pycache__', 'migrations']): continue
        init_file = os.path.join(root, '__init__.py')
        if not os.path.exists(init_file):
            open(init_file, 'w').close()

files = {}

files['requirements.txt'] = r'''
Django==4.2
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
channels==4.0.0
channels-redis==4.1.0
celery==5.3.4
redis==5.0.1
psycopg2-binary==2.9.9
pgvector==0.2.3
django-cors-headers==4.2.0
drf-spectacular==0.26.5
openai==1.3.5
google-generativeai==0.3.1
elevenlabs==0.2.26
google-cloud-texttospeech==2.14.1
google-cloud-speech==2.21.1
twilio==8.10.2
'''

files['manage.py'] = r'''
#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''

files['config/__init__.py'] = r'''
from .celery import app as celery_app

__all__ = ('celery_app',)
'''

files['config/settings/__init__.py'] = r''''''

files['config/settings/base.py'] = r'''
import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'django-insecure-default-key-for-luna-dev'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'channels',
    'drf_spectacular',
    'apps.users',
    'apps.authentication',
    'apps.chat',
    'apps.memory',
    'apps.voice',
    'apps.ai',
    'apps.calls',
    'apps.personality',
    'apps.notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'luna_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],
        },
    },
}

CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

SPECTACULAR_SETTINGS = {
    'TITLE': 'Luna AI Platform API',
    'DESCRIPTION': 'API for Luna AI Voice Companion',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

CORS_ALLOW_ALL_ORIGINS = True
AI_PROVIDER = 'openai'
'''

files['config/settings/development.py'] = r'''
from .base import *
DEBUG = True
'''

files['config/settings/production.py'] = r'''
from .base import *
DEBUG = False
ALLOWED_HOSTS = ['api.luna.ai']
'''

files['config/urls.py'] = r'''
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('api/memory/', include('apps.memory.urls')),
    path('api/voice/', include('apps.voice.urls')),
    path('api/calls/', include('apps.calls.urls')),
    path('api/personality/', include('apps.personality.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
'''

files['config/asgi.py'] = r'''
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
'''

files['config/wsgi.py'] = r'''
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
application = get_wsgi_application()
'''

files['config/celery.py'] = r'''
import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
app = Celery('luna_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
'''

files['apps/users/models.py'] = r'''
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('ur', 'Urdu'),
        ('te', 'Telugu'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
'''

files['apps/users/serializers.py'] = r'''
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'avatar', 'language', 'is_verified', 'created_at']
        read_only_fields = ['id', 'is_verified', 'created_at']
'''

files['apps/users/views.py'] = r'''
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer

class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
'''

files['apps/users/urls.py'] = r'''
from django.urls import path
from .views import UserDetailView

urlpatterns = [
    path('me/', UserDetailView.as_view(), name='user-detail'),
]
'''

files['apps/users/admin.py'] = r'''
from django.contrib import admin
from .models import User
admin.site.register(User)
'''

files['apps/users/tests.py'] = r'''
from django.test import TestCase
class UserTests(TestCase): pass
'''

files['apps/authentication/serializers.py'] = r'''
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
'''

files['apps/authentication/views.py'] = r'''
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)

class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer
    def post(self, request):
        return Response({"message": "Password reset link sent."})

class PasswordResetConfirmView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetConfirmSerializer
    def post(self, request):
        return Response({"message": "Password reset successful."})
'''

files['apps/authentication/urls.py'] = r'''
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, PasswordResetRequestView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
'''
files['apps/authentication/admin.py'] = r'''
from django.contrib import admin
'''
files['apps/authentication/tests.py'] = r'''
from django.test import TestCase
'''


for p, c in files.items(): write_f(p, c)
touch_inits(os.path.join(BASE_DIR, 'apps'))
touch_inits(os.path.join(BASE_DIR, 'config'))
print("Part 1 written successfully.")
