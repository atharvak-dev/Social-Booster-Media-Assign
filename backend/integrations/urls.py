from django.urls import path
from .views import SearchBrandRankingView, APIUsageView, BulkSearchView

urlpatterns = [
    path('search/', SearchBrandRankingView.as_view(), name='search-brand'),
    path('bulk-search/', BulkSearchView.as_view(), name='bulk-search'),
    path('usage/', APIUsageView.as_view(), name='api-usage'),
]
