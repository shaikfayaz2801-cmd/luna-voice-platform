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
