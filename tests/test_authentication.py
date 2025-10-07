"""
Tests for authentication and user management.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration."""
    
    def test_register_student(self, api_client):
        """Test student registration."""
        data = {
            'email': 'newstudent@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'Student',
            'role': 'student'
        }
        response = api_client.post('/api/users/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='newstudent@test.com').exists()
    
    def test_register_teacher(self, api_client):
        """Test teacher registration."""
        data = {
            'email': 'newteacher@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'New',
            'last_name': 'Teacher',
            'role': 'teacher'
        }
        response = api_client.post('/api/users/register/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email='newteacher@test.com').exists()
    
    def test_register_duplicate_email(self, api_client, student_user):
        """Test registration with duplicate email."""
        data = {
            'email': 'student@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Duplicate',
            'last_name': 'User',
            'role': 'student'
        }
        response = api_client.post('/api/users/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_password_mismatch(self, api_client):
        """Test registration with mismatched passwords."""
        data = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'password2': 'differentpass',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'student'
        }
        response = api_client.post('/api/users/register/', data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestUserLogin:
    """Test user login."""
    
    def test_login_success(self, api_client, student_user):
        """Test successful login."""
        data = {
            'email': 'student@test.com',
            'password': 'testpass123'
        }
        response = api_client.post('/api/users/login/', data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_login_invalid_credentials(self, api_client, student_user):
        """Test login with invalid credentials."""
        data = {
            'email': 'student@test.com',
            'password': 'wrongpassword'
        }
        response = api_client.post('/api/users/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_nonexistent_user(self, api_client):
        """Test login with nonexistent user."""
        data = {
            'email': 'nonexistent@test.com',
            'password': 'testpass123'
        }
        response = api_client.post('/api/users/login/', data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile operations."""
    
    def test_get_profile(self, authenticated_client, student_user):
        """Test getting user profile."""
        response = authenticated_client.get('/api/users/profile/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == 'student@test.com'
    
    def test_update_profile(self, authenticated_client, student_user):
        """Test updating user profile."""
        data = {
            'first_name': 'Updated',
            'last_name': 'Name'
        }
        response = authenticated_client.patch('/api/users/profile/', data)
        assert response.status_code == status.HTTP_200_OK
        student_user.refresh_from_db()
        assert student_user.first_name == 'Updated'
    
    def test_unauthenticated_profile_access(self, api_client):
        """Test accessing profile without authentication."""
        response = api_client.get('/api/users/profile/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestTokenRefresh:
    """Test JWT token refresh."""
    
    def test_refresh_token(self, api_client, student_user):
        """Test refreshing access token."""
        # Login to get tokens
        login_data = {
            'email': 'student@test.com',
            'password': 'testpass123'
        }
        login_response = api_client.post('/api/users/login/', login_data)
        refresh_token = login_response.data['refresh']
        
        # Refresh token
        refresh_data = {'refresh': refresh_token}
        response = api_client.post('/api/users/token/refresh/', refresh_data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data