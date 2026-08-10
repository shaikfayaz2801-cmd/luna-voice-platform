import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestIntegrationPipeline:
    """Integration test simulating the flow of user registration to conversation creation."""

    def test_end_to_end_auth_and_chat(self, api_client):
        # 1. Register User
        register_url = reverse('register')
        register_data = {
            "email": "integration@example.com",
            "password": "strongpassword123",
            "first_name": "Integration",
            "last_name": "Test"
        }
        reg_response = api_client.post(register_url, register_data)
        assert reg_response.status_code == 201
        
        # 2. Login User
        login_url = reverse('token_obtain_pair')
        login_data = {
            "email": "integration@example.com",
            "password": "strongpassword123"
        }
        login_response = api_client.post(login_url, login_data)
        assert login_response.status_code == 200
        access_token = login_response.data['access']
        
        # 3. Authenticate Client
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # 4. Create Conversation
        conv_url = reverse('conversation-list')
        conv_data = {"title": "E2E Test Chat"}
        conv_response = api_client.post(conv_url, conv_data)
        assert conv_response.status_code == 201
        conv_id = conv_response.data['id']
        
        # 5. Verify Conversation Exists
        conv_list_response = api_client.get(conv_url)
        assert conv_list_response.status_code == 200
        assert len(conv_list_response.data['results']) == 1
        assert str(conv_list_response.data['results'][0]['id']) == str(conv_id)
