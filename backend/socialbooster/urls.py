"""
URL configuration for SocialBooster project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import os

def serve_react(request):
    """Serve React app index.html for all non-API routes"""
    index_path = os.path.join(settings.STATIC_ROOT, 'index.html')
    try:
        with open(index_path, 'r') as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('App loading...', status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication endpoints
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('users.urls')),
    
    # API endpoints
    path('api/brands/', include('brands.urls')),
    path('api/rankings/', include('rankings.urls')),
    path('api/citations/', include('citations.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/integrations/', include('integrations.urls')),
    
    # Serve React app for all other routes (exclude api/, admin/, static/, assets/)
    re_path(r'^(?!api/|admin/|static/|assets/).*$', serve_react),
]
