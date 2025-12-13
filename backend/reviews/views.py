from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Sum, Count
from django.db.models.functions import Coalesce
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review CRUD and analytics.
    
    Optimizations applied:
    - select_related('brand') for foreign key eager loading
    - Single aggregate query for summary
    """
    queryset = Review.objects.select_related('brand').all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        brand_id = self.request.query_params.get('brand')
        platform = self.request.query_params.get('platform')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if platform:
            queryset = queryset.filter(platform=platform)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get review summary statistics.
        Optimized: Single aggregate query for stats.
        """
        queryset = self.get_queryset()
        
        # Single aggregate query for overall stats
        stats = queryset.aggregate(
            avg_rating=Coalesce(Avg('rating'), 0.0),
            total_reviews=Coalesce(Sum('review_count'), 0)
        )
        
        # Group by platform (efficient values + annotate)
        by_platform = queryset.values('platform').annotate(
            avg_rating=Avg('rating'),
            total_reviews=Sum('review_count'),
            count=Count('id')
        ).order_by('-avg_rating')
        
        platform_names = dict(Review.PLATFORM_CHOICES)
        result = []
        for item in by_platform:
            result.append({
                'platform': item['platform'],
                'platform_display': platform_names.get(item['platform'], item['platform']),
                'avg_rating': round(float(item['avg_rating'] or 0), 1),
                'total_reviews': item['total_reviews'] or 0
            })
        
        return Response({
            'average_rating': round(float(stats['avg_rating']), 1),
            'total_reviews': stats['total_reviews'],
            'by_platform': result
        })
