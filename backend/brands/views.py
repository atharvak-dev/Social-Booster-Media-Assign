from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Brand
from .serializers import BrandSerializer
from .auto_fetch import auto_fetch_brand_data
import threading


class BrandViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Brand CRUD operations.
    
    list: GET /api/brands/
    create: POST /api/brands/
    retrieve: GET /api/brands/{id}/
    update: PUT /api/brands/{id}/
    partial_update: PATCH /api/brands/{id}/
    destroy: DELETE /api/brands/{id}/
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a brand and automatically fetch real data from the internet."""
        response = super().create(request, *args, **kwargs)
        
        if response.status_code == 201:
            # Get the created brand
            brand_id = response.data.get('id')
            try:
                brand = Brand.objects.get(id=brand_id)
                # Run auto-fetch in background thread to avoid blocking the response
                thread = threading.Thread(target=auto_fetch_brand_data, args=(brand,))
                thread.start()
                
                # Add message to response indicating data fetch is in progress
                response.data['auto_fetch_status'] = 'Data fetching started in background'
            except Brand.DoesNotExist:
                pass
        
        return response
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        brand_name = instance.name
        self.perform_destroy(instance)
        return Response(
            {'message': f'Brand "{brand_name}" deleted successfully'},
            status=status.HTTP_200_OK
        )
