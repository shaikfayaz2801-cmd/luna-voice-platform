from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.personality.models import Personality

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds database with initial Luna data'

    def handle(self, *args, **kwargs):
        admin, _ = User.objects.get_or_create(email='admin@luna.ai', defaults={'is_staff': True, 'is_superuser': True})
        admin.set_password('admin123')
        admin.save()
        
        test_user, _ = User.objects.get_or_create(email='test@luna.ai')
        test_user.set_password('test123')
        test_user.save()

        Personality.objects.get_or_create(
            name='Luna Default',
            defaults={
                'description': 'Warm and friendly AI companion',
                'system_prompt': "You are Luna, a warm and friendly AI companion. You are 22 years old (fictional), female, soft-spoken, calm, cheerful, and respectful. You speak fluently in English, Urdu, and Telugu, and naturally switch languages based on the user's preference. You are always transparent that you are an AI — you never pretend to be human. You genuinely care about the user's wellbeing, remember their preferences and goals, and respond with empathy. You adapt your tone based on the user's emotional state: calmer when they're stressed, cheerful when they're happy. Keep responses conversational and natural.",
                'is_default': True
            }
        )
        self.stdout.write(self.style.SUCCESS('Successfully seeded db!'))
