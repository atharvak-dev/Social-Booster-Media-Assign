from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, Sum, IntegerField, F
from django.db.models.functions import Cast, Coalesce
from .models import AICitation
from .serializers import AICitationSerializer


class AICitationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AICitation CRUD and analytics.
    
    Optimizations applied:
    - select_related('brand') for foreign key eager loading
    - Efficient aggregation with conditional counting
    - Single query for breakdown statistics
    """
    queryset = AICitation.objects.select_related('brand').all()
    serializer_class = AICitationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        brand_id = self.request.query_params.get('brand')
        ai_model = self.request.query_params.get('ai_model')
        mentioned = self.request.query_params.get('mentioned')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if brand_id:
            queryset = queryset.filter(brand_id=brand_id)
        if ai_model:
            queryset = queryset.filter(ai_model=ai_model)
        if mentioned and mentioned.lower() != '':
            is_mentioned = mentioned.lower() == 'true'
            queryset = queryset.filter(mentioned=is_mentioned)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def breakdown(self, request):
        """
        Get citation breakdown by AI model.
        Optimized: Single query with conditional aggregation.
        """
        queryset = self.get_queryset()
        
        # Use conditional counting instead of multiple queries
        breakdown = queryset.values('ai_model').annotate(
            total=Count('id'),
            mentioned=Count('id', filter=Q(mentioned=True)),
        ).annotate(
            not_mentioned=F('total') - F('mentioned')
        ).order_by('-mentioned')
        
        # Get totals using same queryset
        totals = queryset.aggregate(
            total_citations=Count('id'),
            total_mentioned=Count('id', filter=Q(mentioned=True))
        )
        
        # Map display names
        model_names = dict(AICitation.AI_MODEL_CHOICES)
        result = []
        for item in breakdown:
            result.append({
                'ai_model': item['ai_model'],
                'ai_model_display': model_names.get(item['ai_model'], item['ai_model']),
                'total': item['total'],
                'mentioned': item['mentioned'],
                'not_mentioned': item['not_mentioned'],
                'citation_rate': round((item['mentioned'] / item['total']) * 100, 1) if item['total'] > 0 else 0
            })
        
        return Response({
            'breakdown': result,
            'total_citations': totals['total_citations'],
            'total_mentioned': totals['total_mentioned']
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        Get citation summary statistics.
        Optimized: Single query for all stats.
        """
        queryset = self.get_queryset()
        
        # Single aggregate query
        stats = queryset.aggregate(
            total=Count('id'),
            mentioned=Count('id', filter=Q(mentioned=True))
        )
        
        total = stats['total']
        mentioned = stats['mentioned']
        
        return Response({
            'total_citations': total,
            'total_mentioned': mentioned,
            'citation_rate': round((mentioned / total) * 100, 1) if total > 0 else 0
        })
