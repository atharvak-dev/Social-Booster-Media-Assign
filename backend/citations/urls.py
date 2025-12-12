from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AICitationViewSet

router = DefaultRouter()
router.register(r'', AICitationViewSet, basename='citation')

urlpatterns = [
    path('', include(router.urls)),
]
