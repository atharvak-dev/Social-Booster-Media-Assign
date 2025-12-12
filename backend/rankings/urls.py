from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SearchRankingViewSet

router = DefaultRouter()
router.register(r'', SearchRankingViewSet, basename='ranking')

urlpatterns = [
    path('', include(router.urls)),
]
