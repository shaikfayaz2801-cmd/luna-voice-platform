import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from apps.chat.models import Conversation, Message

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="chatuser@example.com",
        password="password123",
        first_name="Chat",
        last_name="User"
    )

@pytest.fixture
def test_conversation(test_user):
    return Conversation.objects.create(user=test_user, title="Test Chat")

@pytest.mark.django_db
class TestChat:
    
    def test_list_conversations(self, authenticated_client, test_conversation):
        url = reverse('conversation-list')
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Test Chat"

    def test_create_conversation(self, authenticated_client):
        url = reverse('conversation-list')
        data = {"title": "New Chat"}
        response = authenticated_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == "New Chat"

    def test_archive_conversation(self, authenticated_client, test_conversation):
        url = reverse('conversation-archive', kwargs={'pk': test_conversation.id})
        response = authenticated_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        test_conversation.refresh_from_db()
        assert test_conversation.is_archived is True

    def test_list_messages_unauthorized(self, api_client, test_conversation):
        url = reverse('message-list', kwargs={'conversation_id': test_conversation.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
