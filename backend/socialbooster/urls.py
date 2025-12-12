"""
URL configuration for SocialBooster project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/brands/', include('brands.urls')),
    path('api/rankings/', include('rankings.urls')),
    path('api/citations/', include('citations.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/integrations/', include('integrations.urls')),
]
