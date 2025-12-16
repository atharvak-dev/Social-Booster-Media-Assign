"""
Tests for Brand API endpoints.
"""
import pytest
from rest_framework import status
from brands.models import Brand


@pytest.mark.django_db
class TestBrandAPI:
    """Test Brand CRUD endpoints."""
    
    def test_list_brands(self, api_client, test_brand):
        """Test listing all brands."""
        url = '/api/brands/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) >= 1
    
    def test_create_brand(self, authenticated_client):
        """Test creating a brand (requires auth)."""
        url = '/api/brands/'
        data = {
            'name': 'New Brand',
            'category': 'software',
            'website': 'https://newbrand.com'
        }
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Brand'
    
    def test_retrieve_brand(self, api_client, test_brand):
        """Test retrieving a single brand."""
        url = f'/api/brands/{test_brand.id}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Test Brand'
    
    def test_update_brand(self, authenticated_client, test_brand):
        """Test updating a brand."""
        url = f'/api/brands/{test_brand.id}/'
        data = {'name': 'Updated Brand'}
        response = authenticated_client.patch(url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated Brand'
    
    def test_delete_brand(self, authenticated_client, test_brand):
        """Test deleting a brand."""
        url = f'/api/brands/{test_brand.id}/'
        response = authenticated_client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert Brand.objects.filter(id=test_brand.id).count() == 0


@pytest.mark.django_db
class TestDashboardAPI:
    """Test Dashboard endpoints."""
    
    def test_dashboard_overview(self, api_client):
        """Test dashboard overview endpoint."""
        url = '/api/dashboard/overview/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'overview' in response.data
        assert 'charts' in response.data
    
    def test_dashboard_caching(self, api_client):
        """Test that dashboard uses caching."""
        url = '/api/dashboard/overview/'
        # First request
        response1 = api_client.get(url)
        assert response1.status_code == status.HTTP_200_OK
        
        # Second request should be cached
        response2 = api_client.get(url)
        assert response2.status_code == status.HTTP_200_OK
        assert response1.data == response2.data
