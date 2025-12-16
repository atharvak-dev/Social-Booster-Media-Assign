"""
Tests for authentication endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAuthentication:
    """Test JWT authentication endpoints."""
    
    def test_register_user(self, api_client):
        """Test user registration."""
        url = '/api/auth/register/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password2': 'SecurePass123!',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert response.data['user']['username'] == 'newuser'
    
    def test_register_password_mismatch(self, api_client):
        """Test registration fails with password mismatch."""
        url = '/api/auth/register/'
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123!',
            'password2': 'DifferentPass123!',
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_obtain_token(self, api_client, test_user):
        """Test JWT token generation."""
        url = '/api/auth/token/'
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_token_refresh(self, api_client, test_user):
        """Test JWT token refresh."""
        # Get initial tokens
        token_url = '/api/auth/token/'
        token_response = api_client.post(token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        refresh_token = token_response.data['refresh']
        
        # Refresh the token
        refresh_url = '/api/auth/token/refresh/'
        response = api_client.post(refresh_url, {'refresh': refresh_token}, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_protected_endpoint_without_auth(self, api_client):
        """Test that protected endpoints require authentication."""
        url = '/api/auth/profile/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_protected_endpoint_with_auth(self, authenticated_client):
        """Test accessing protected endpoint with valid token."""
        url = '/api/auth/profile/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'
