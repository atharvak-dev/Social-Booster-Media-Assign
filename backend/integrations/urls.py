from django.urls import path
from .views import (
    SearchBrandRankingView, APIUsageView, BulkSearchView,
    GeminiTestView, GeminiCitationCheckView
)

urlpatterns = [
    path('search/', SearchBrandRankingView.as_view(), name='search-brand'),
    path('bulk-search/', BulkSearchView.as_view(), name='bulk-search'),
    path('usage/', APIUsageView.as_view(), name='api-usage'),
    path('gemini/test/', GeminiTestView.as_view(), name='gemini-test'),
    path('gemini/check-citation/', GeminiCitationCheckView.as_view(), name='gemini-check-citation'),
]
