from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q, F
from datetime import date, timedelta
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
    
    @action(detail=False, methods=['get'])
    def timeline(self, request):
        """Get citation trends over time for timeline graphs."""
        days = int(request.query_params.get('days', 14))
        group_by = request.query_params.get('group_by', 'ai_model')  # 'ai_model' or 'brand'
        
        end_date = date.today()
        start_date = end_date - timedelta(days=days - 1)
        
        # Generate all dates in range
        dates = [(start_date + timedelta(days=i)).isoformat() for i in range(days)]
        
        queryset = AICitation.objects.filter(date__gte=start_date, date__lte=end_date)
        
        if group_by == 'brand':
            # Group by brand over time
            data = queryset.values('date', 'brand__name').annotate(
                total=Count('id'),
                mentioned=Count('id', filter=Q(mentioned=True))
            ).order_by('date')
            
            # Organize by brand
            brands = {}
            for item in data:
                brand_name = item['brand__name']
                if brand_name not in brands:
                    brands[brand_name] = {d: {'total': 0, 'mentioned': 0} for d in dates}
                brands[brand_name][item['date'].isoformat()] = {
                    'total': item['total'],
                    'mentioned': item['mentioned']
                }
            
            # Format for chart.js
            datasets = []
            colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#06B6D4', '#84CC16']
            for idx, (brand_name, date_data) in enumerate(brands.items()):
                mentioned_data = [date_data[d]['mentioned'] for d in dates]
                total_data = [date_data[d]['total'] for d in dates]
                rate_data = [
                    round(m / t * 100, 1) if t > 0 else 0 
                    for m, t in zip(mentioned_data, total_data)
                ]
                datasets.append({
                    'label': brand_name,
                    'data': rate_data,
                    'borderColor': colors[idx % len(colors)],
                    'tension': 0.3
                })
        else:
            # Group by AI model over time
            data = queryset.values('date', 'ai_model').annotate(
                total=Count('id'),
                mentioned=Count('id', filter=Q(mentioned=True))
            ).order_by('date')
            
            model_names = dict(AICitation.AI_MODEL_CHOICES)
            models = {}
            for item in data:
                model = item['ai_model']
                if model not in models:
                    models[model] = {d: {'total': 0, 'mentioned': 0} for d in dates}
                models[model][item['date'].isoformat()] = {
                    'total': item['total'],
                    'mentioned': item['mentioned']
                }
            
            # Format for chart.js
            datasets = []
            model_colors = {
                'chatgpt': '#10A37F',
                'gemini': '#4285F4',
                'perplexity': '#8B5CF6',
                'copilot': '#00A4EF',
                'claude': '#D97757',
                'google_ai': '#EA4335'
            }
            for model, date_data in models.items():
                mentioned_data = [date_data[d]['mentioned'] for d in dates]
                total_data = [date_data[d]['total'] for d in dates]
                rate_data = [
                    round(m / t * 100, 1) if t > 0 else 0 
                    for m, t in zip(mentioned_data, total_data)
                ]
                datasets.append({
                    'label': model_names.get(model, model),
                    'data': rate_data,
                    'borderColor': model_colors.get(model, '#6B7280'),
                    'tension': 0.3
                })
        
        return Response({
            'labels': dates,
            'datasets': datasets,
            'period': f'{days} days',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        })
