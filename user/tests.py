import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .factories import UserFactory
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

@pytest.fixture
def api_client():
    """Fixture to provide an API client for testing."""
    return APIClient()

@pytest.fixture
def test_user(db):
    """Fixture to create a user instance in the database."""
    return UserFactory(username="testuser")

@pytest.fixture
def auth_tokens(api_client, test_user):
    """Fixture to obtain authentication tokens for a test user."""
    response = api_client.post('/api/user/token/', {
        'username': test_user.username,
        'password': 'securepassword123',
    })
    return response.data

def test_signup_success(api_client):
    """Test user signup with valid data."""
    response = api_client.post('/api/user/signup/', {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'securepassword123',
    })
    assert response.status_code == 201
    assert 'username' in response.data
    assert response.data['username'] == 'newuser'

def test_signup_missing_fields(api_client):
    """Test signup with missing required fields."""
    response = api_client.post('/api/user/signup/', {'username': 'newuser'})
    assert response.status_code == 400

def test_token_obtain_success(api_client, test_user):
    """Test obtaining token with valid credentials."""
    response = api_client.post('/api/user/token/', {
        'username': test_user.username,
        'password': 'securepassword123',
    })
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

def test_token_obtain_invalid_credentials(api_client, test_user):
    """Test obtaining token with invalid credentials."""
    response = api_client.post('/api/user/token/', {
        'username': test_user.username,
        'password': 'wrongpassword',
    })
    assert response.status_code == 401

def test_token_refresh_success(api_client, auth_tokens):
    """Test refreshing token with a valid refresh token."""
    refresh_token = auth_tokens['refresh']
    response = api_client.post('/api/user/token/refresh/', {'refresh': refresh_token})
    assert response.status_code == 200
    assert 'access' in response.data

def test_token_refresh_invalid_token(api_client):
    """Test refreshing token with an invalid refresh token."""
    response = api_client.post('/api/user/token/refresh/', {'refresh': 'invalid_token'})
    assert response.status_code == 401
    assert 'detail' in response.data
