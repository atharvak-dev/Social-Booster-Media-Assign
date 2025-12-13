"""
URL configuration for SocialBooster project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/brands/', include('brands.urls')),
    path('api/rankings/', include('rankings.urls')),
    path('api/citations/', include('citations.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/integrations/', include('integrations.urls')),
    # Serve React app for all other routes
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]

# Serve static files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

