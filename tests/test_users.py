"""
Tests for user authentication and management.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        full_name='Test User',
        role='student'
    )


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration."""
    
    def test_register_student(self, api_client):
        """Test student registration."""
        data = {
            'email': 'student@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'full_name': 'Test Student',
            'role': 'student'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data['data']
        assert 'tokens' in response.data['data']
    
    def test_register_teacher(self, api_client):
        """Test teacher registration."""
        data = {
            'email': 'teacher@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'full_name': 'Test Teacher',
            'role': 'teacher'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
    
    def test_register_password_mismatch(self, api_client):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'different',
            'full_name': 'Test User',
            'role': 'student'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    """Test user login."""
    
    def test_login_success(self, api_client, test_user):
        """Test successful login."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'tokens' in response.data['data']
    
    def test_login_invalid_credentials(self, api_client, test_user):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile management."""
    
    def test_get_profile(self, api_client, test_user):
        """Test getting user profile."""
        api_client.force_authenticate(user=test_user)
        response = api_client.get('/api/auth/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['data']['email'] == test_user.email
    
    def test_update_profile(self, api_client, test_user):
        """Test updating user profile."""
        api_client.force_authenticate(user=test_user)
        data = {'full_name': 'Updated Name'}
        response = api_client.put('/api/auth/profile/update/', data)
        assert response.status_code == status.HTTP_200_OK
        test_user.refresh_from_db()
        assert test_user.full_name == 'Updated Name'