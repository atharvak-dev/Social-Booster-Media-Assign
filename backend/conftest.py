"""
Pytest configuration and fixtures for testing.
"""
import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from brands.models import Brand


@pytest.fixture
def api_client():
    """Return an unauthenticated API client."""
    return APIClient()


@pytest.fixture
def authenticated_client(db):
    """Return an authenticated API client."""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def test_user(db):
    """Create a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )


@pytest.fixture
def test_brand(db):
    """Create a test brand."""
    return Brand.objects.create(
        name='Test Brand',
        category='software',
        website='https://testbrand.com'
    )
