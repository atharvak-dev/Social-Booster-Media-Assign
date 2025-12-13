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
    try:
        with open(os.path.join(settings.STATIC_ROOT, 'index.html')) as f:
            return HttpResponse(f.read(), content_type='text/html')
    except FileNotFoundError:
        return HttpResponse('React app not built. Run: cd frontend && npm run build', status=404)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/brands/', include('brands.urls')),
    path('api/rankings/', include('rankings.urls')),
    path('api/citations/', include('citations.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/integrations/', include('integrations.urls')),
    # Serve React app for all other routes
    re_path(r'^(?!api/).*$', serve_react),
]

