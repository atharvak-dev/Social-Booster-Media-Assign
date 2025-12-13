from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, F
from .models import AICitation
from .serializers import AICitationSerializer


class AICitationViewSet(viewsets.ModelViewSet):
    """ViewSet for AICitation CRUD and analytics."""
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
        """Get citation breakdown by AI model."""
        queryset = self.get_queryset()
        
        breakdown = queryset.values('ai_model').annotate(
            total=Count('id'),
            mentioned=Count('id', filter=Q(mentioned=True)),
        ).annotate(
            not_mentioned=F('total') - F('mentioned')
        ).order_by('-mentioned')
        
        total_citations = queryset.count()
        total_mentioned = queryset.filter(mentioned=True).count()
        
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
            'total_citations': total_citations,
            'total_mentioned': total_mentioned
        })
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get citation summary statistics."""
        queryset = self.get_queryset()
        total = queryset.count()
        mentioned = queryset.filter(mentioned=True).count()
        
        return Response({
            'total_citations': total,
            'total_mentioned': mentioned,
            'citation_rate': round((mentioned / total) * 100, 1) if total > 0 else 0
        })
