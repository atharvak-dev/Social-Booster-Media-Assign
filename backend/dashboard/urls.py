from django.urls import path
from .views import DashboardOverviewView, ExportDataView

urlpatterns = [
    path('overview/', DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('export/', ExportDataView.as_view(), name='export-data'),
]
