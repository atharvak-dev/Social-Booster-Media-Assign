from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import SearchRanking
from .serializers import SearchRankingSerializer


class SearchRankingViewSet(viewsets.ModelViewSet):
    """ViewSet for SearchRanking CRUD and trend analysis."""
    queryset = SearchRanking.objects.select_related('brand').all()
    serializer_class = SearchRankingSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        brand_id = self.request.query_params.get('brand')
        keyword = self.request.query_params.get('keyword')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if keyword:
            queryset = queryset.filter(keyword__icontains=keyword)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'], url_path='trends/(?P<brand_id>[^/.]+)')
    def trends(self, request, brand_id=None):
        """Get ranking trends for a specific brand."""
        rankings = SearchRanking.objects.filter(brand_id=brand_id).order_by('date')
        trend_data = {}
        for ranking in rankings:
            keyword = ranking.keyword
            if keyword not in trend_data:
                trend_data[keyword] = []
            trend_data[keyword].append({
                'date': ranking.date.isoformat(),
                'position': ranking.position
            })
        return Response({'brand_id': brand_id, 'trends': trend_data})
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get ranking summary statistics."""
        queryset = self.get_queryset()
        avg_position = queryset.aggregate(avg=Avg('position'))['avg'] or 0
        
        return Response({
            'total_rankings': queryset.count(),
            'average_position': round(avg_position, 1),
            'unique_keywords': queryset.values('keyword').distinct().count()
        })
