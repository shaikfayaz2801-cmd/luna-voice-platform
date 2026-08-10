import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="password123",
        first_name="Test",
        last_name="User"
    )

@pytest.mark.django_db
class TestAuthentication:
    
    def test_user_registration(self, api_client):
        url = reverse('register')
        data = {
            "email": "newuser@example.com",
            "password": "securepassword",
            "first_name": "New",
            "last_name": "User"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert User.objects.filter(email="newuser@example.com").exists()

    def test_user_login(self, api_client, test_user):
        url = reverse('token_obtain_pair')
        data = {
            "email": "testuser@example.com",
            "password": "password123"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_invalid_login(self, api_client, test_user):
        url = reverse('token_obtain_pair')
        data = {
            "email": "testuser@example.com",
            "password": "wrongpassword"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
