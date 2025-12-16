from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Avg, Count, Sum, Q
from django.core.cache import cache
from brands.models import Brand
from rankings.models import SearchRanking
from citations.models import AICitation
from reviews.models import Review


class DashboardOverviewView(APIView):
    """Dashboard overview with aggregated statistics. Cached for 5 minutes."""
    permission_classes = [AllowAny]  # Dashboard is public
    
    def get(self, request):
        start_date = request.query_params.get('start_date') or None
        end_date = request.query_params.get('end_date') or None
        
        # Create cache key based on date filters
        cache_key = f'dashboard_{start_date}_{end_date}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        total_brands = Brand.objects.count()
        
        # Rankings stats
        rankings_qs = SearchRanking.objects.all()
        if start_date:
            rankings_qs = rankings_qs.filter(date__gte=start_date)
        if end_date:
            rankings_qs = rankings_qs.filter(date__lte=end_date)
        avg_position = rankings_qs.aggregate(avg=Avg('position'))['avg'] or 0
        
        # Citations stats
        citations_qs = AICitation.objects.all()
        if start_date:
            citations_qs = citations_qs.filter(date__gte=start_date)
        if end_date:
            citations_qs = citations_qs.filter(date__lte=end_date)
        total_citations = citations_qs.count()
        mentioned_citations = citations_qs.filter(mentioned=True).count()
        citation_rate = round((mentioned_citations / total_citations) * 100, 1) if total_citations > 0 else 0
        
        # Reviews stats
        reviews_qs = Review.objects.all()
        if start_date:
            reviews_qs = reviews_qs.filter(date__gte=start_date)
        if end_date:
            reviews_qs = reviews_qs.filter(date__lte=end_date)
        avg_rating = reviews_qs.aggregate(avg=Avg('rating'))['avg'] or 0
        total_reviews = reviews_qs.aggregate(total=Sum('review_count'))['total'] or 0
        
        data = {
            'overview': {
                'total_brands': total_brands,
                'average_search_position': round(avg_position, 1),
                'ai_citation_rate': citation_rate,
                'average_rating': round(float(avg_rating), 1),
                'total_reviews': total_reviews,
            },
            'charts': {
                'ranking_summary': self._get_ranking_chart_data(),
                'citation_breakdown': self._get_citation_breakdown(),
                'brand_comparison': self._get_brand_comparison(),
            }
        }
        
        # Cache for 5 minutes
        cache.set(cache_key, data, 300)
        
        return Response(data)
    
    def _get_ranking_chart_data(self):
        """Get ranking data for line chart."""
        brands = Brand.objects.all()[:5]
        chart_data = []
        for brand in brands:
            rankings = SearchRanking.objects.filter(brand=brand).order_by('date')[:30]
            chart_data.append({
                'brand_name': brand.name,
                'data': [{'date': r.date.isoformat(), 'position': r.position} for r in rankings]
            })
        return chart_data
    
    def _get_citation_breakdown(self):
        """Get citation data for pie chart."""
        breakdown = AICitation.objects.filter(mentioned=True).values('ai_model').annotate(
            count=Count('id')
        ).order_by('-count')
        model_names = dict(AICitation.AI_MODEL_CHOICES)
        return [
            {'name': model_names.get(item['ai_model'], item['ai_model']), 'value': item['count']}
            for item in breakdown
        ]
    
    def _get_brand_comparison(self):
        """Get brand visibility scores for bar chart."""
        brands = Brand.objects.all()
        comparison = []
        for brand in brands:
            avg_position = brand.rankings.aggregate(avg=Avg('position'))['avg'] or 100
            citation_rate = 0
            total_citations = brand.citations.count()
            if total_citations > 0:
                mentioned = brand.citations.filter(mentioned=True).count()
                citation_rate = (mentioned / total_citations) * 100
            avg_rating = brand.reviews.aggregate(avg=Avg('rating'))['avg'] or 0
            
            position_score = max(0, 100 - float(avg_position))
            visibility_score = (position_score * 0.4) + (citation_rate * 0.4) + (float(avg_rating) * 4)
            
            comparison.append({
                'brand_name': brand.name,
                'visibility_score': round(visibility_score, 1),
                'search_score': round(position_score, 1),
                'ai_score': round(citation_rate, 1),
                'review_score': round(float(avg_rating) * 20, 1)
            })
        return sorted(comparison, key=lambda x: x['visibility_score'], reverse=True)


class ExportDataView(APIView):
    """Export data as JSON."""
    permission_classes = [AllowAny]
    
    def get(self, request):
        brand_id = request.query_params.get('brand')
        data = {'brands': list(Brand.objects.values())}
        
        if brand_id:
            data['rankings'] = list(SearchRanking.objects.filter(brand_id=brand_id).values())
            data['citations'] = list(AICitation.objects.filter(brand_id=brand_id).values())
            data['reviews'] = list(Review.objects.filter(brand_id=brand_id).values())
        else:
            data['rankings'] = list(SearchRanking.objects.values())
            data['citations'] = list(AICitation.objects.values())
            data['reviews'] = list(Review.objects.values())
        
        return Response(data)
