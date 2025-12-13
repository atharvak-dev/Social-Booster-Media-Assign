"""
URL configuration for SocialBooster project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
import os

def serve_react(request, path=''):
    """Serve React app index.html for all non-API routes"""
    index_path = os.path.join(settings.STATIC_ROOT, 'index.html')
    return serve(request, 'index.html', document_root=settings.STATIC_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/brands/', include('brands.urls')),
    path('api/rankings/', include('rankings.urls')),
    path('api/citations/', include('citations.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/integrations/', include('integrations.urls')),
    # Serve React app for all other routes
    re_path(r'^.*$', serve_react, name='react'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
