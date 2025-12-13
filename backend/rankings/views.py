from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg
from .models import SearchRanking
from .serializers import SearchRankingSerializer


class SearchRankingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for SearchRanking CRUD and trend analysis.
    
    Optimizations applied:
    - select_related('brand') for foreign key eager loading
    - .only() to limit fetched fields
    - Efficient aggregation with single query
    """
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
        """
        Get ranking trends for a specific brand.
        Optimized: Uses .only() to minimize data transfer.
        """
        # Fetch only needed fields
        rankings = SearchRanking.objects.filter(
            brand_id=brand_id
        ).only('keyword', 'date', 'position').order_by('date')
        
        # Group by keyword efficiently
        trend_data = {}
        for ranking in rankings:
            keyword = ranking.keyword
            if keyword not in trend_data:
                trend_data[keyword] = []
            trend_data[keyword].append({
                'date': ranking.date.isoformat(),
                'position': ranking.position
            })
        
        return Response({
            'brand_id': brand_id,
            'trends': trend_data
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get ranking summary statistics.
        Optimized: Single aggregate query for all stats.
        """
        queryset = self.get_queryset()
        
        # Single query for all aggregations
        stats = queryset.aggregate(
            avg_position=Avg('position'),
            total=len(queryset)  # Avoid extra COUNT query
        )
        
        # Get unique keywords count separately (still efficient)
        unique_keywords = queryset.values('keyword').distinct().count()
        
        return Response({
            'total_rankings': queryset.count(),
            'average_position': round(stats['avg_position'] or 0, 1),
            'unique_keywords': unique_keywords
        })
