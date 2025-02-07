import pytest
from user.factories import UserFactory
from factories import ContentFactory, RateFactory
from math import exp
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock



@pytest.fixture
def api_client():
    """Provides an API client."""
    return APIClient()

@pytest.fixture
def test_user(db):
    """Creates a test user in the database."""
    return UserFactory()

@pytest.fixture
def authenticated_client(api_client, test_user):
    """Logs in the user and provides an authenticated client."""
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def test_content(db, test_user):
    """Creates test content associated with the test user."""
    return ContentFactory(user=test_user)

@pytest.fixture
def test_rate(db, test_user, test_content):
    """Creates a test rating for a content."""
    return RateFactory(user=test_user, post=test_content)

def test_create_content(authenticated_client):
    """Test creating new content successfully."""
    data = {"title": "Test Title", "text": "This is test content."}
    response = authenticated_client.post('/api/content/', data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['title'] == data['title']

def test_create_content_unauthenticated(api_client):
    """Test unauthorized users cannot create content."""
    data = {"title": "Unauthorized", "text": "Should not be created"}
    response = api_client.post('/api/content/', data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_list_content(authenticated_client, test_content):
    """Test listing content with pagination."""
    response = authenticated_client.get('/api/content/')
    assert response.status_code == status.HTTP_200_OK
    assert 'results' in response.data
    assert len(response.data['results']) >= 1

@patch('redis.StrictRedis')
def test_create_rate(mock_redis, authenticated_client, test_content):
    """Test creating a rating successfully."""
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.incr.return_value = 1
    mock_redis_instance.expire.return_value = None

    data = {"score": 5, "post": test_content.id}
    response = authenticated_client.post('/api/rate/', data)
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert response.data["message"] == "Rating has been subscribed."

def test_create_rate_invalid_data(authenticated_client):
    """Test rating creation fails with invalid data."""
    data = {"score": "invalid", "post": "invalid"}
    response = authenticated_client.post('/api/rate/', data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_rate_unauthenticated(api_client, test_content):
    """Test unauthenticated users cannot rate content."""
    data = {"score": 4, "post": test_content.id}
    response = api_client.post('/api/rate/', data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@patch('redis.StrictRedis')
def test_calculate_weight(mock_redis, authenticated_client, test_content):
    """Test weight calculation for rating."""
    mock_redis_instance = MagicMock()
    mock_redis.return_value = mock_redis_instance
    mock_redis_instance.incr.return_value = 10  
    mock_redis_instance.expire.return_value = None

    expected_weight = exp(-0.1 * 10)  

    response = authenticated_client.post('/api/rate/', {"score": 5, "post": test_content.id})
    assert response.status_code == status.HTTP_202_ACCEPTED
    assert mock_redis_instance.incr.called
    assert abs(expected_weight - exp(-0.1 * 10)) < 0.0001



