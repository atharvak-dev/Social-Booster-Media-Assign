from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Avg, Sum
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for Review CRUD and analytics."""
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
        """Get review summary statistics."""
        queryset = self.get_queryset()
        avg_rating = queryset.aggregate(avg=Avg('rating'))['avg'] or 0
        total_reviews = queryset.aggregate(total=Sum('review_count'))['total'] or 0
        
        by_platform = queryset.values('platform').annotate(
            avg_rating=Avg('rating'),
            total_reviews=Sum('review_count')
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
            'average_rating': round(float(avg_rating), 1),
            'total_reviews': total_reviews,
            'by_platform': result
        })
