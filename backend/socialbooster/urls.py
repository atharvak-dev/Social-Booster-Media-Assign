"""
URL configuration for SocialBooster project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from django.conf import settings
import os

def serve_react(request):
    """Serve React app index.html for all non-API routes"""
    index_path = os.path.join(settings.STATIC_ROOT, 'index.html')
    
    # Debug: Log the path we're trying to access
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Trying to serve: {index_path}")
    logger.error(f"STATIC_ROOT: {settings.STATIC_ROOT}")
    logger.error(f"File exists: {os.path.exists(index_path)}")
    
    # List files in STATIC_ROOT for debugging
    if os.path.exists(settings.STATIC_ROOT):
        files = os.listdir(settings.STATIC_ROOT)
        logger.error(f"Files in STATIC_ROOT: {files[:10]}")  # First 10 files
    
    try:
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError as e:
        return HttpResponse(f'File not found: {index_path}<br>Error: {str(e)}', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/brands/', include('brands.urls')),
    path('api/rankings/', include('rankings.urls')),
    path('api/citations/', include('citations.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/integrations/', include('integrations.urls')),
    # Serve React app for all other routes (exclude api/, admin/, static/, assets/)
    re_path(r'^(?!api/|admin/|static/|assets/).*$', serve_react),
]

