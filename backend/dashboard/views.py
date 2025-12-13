from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Count, Sum, Q, Case, When, FloatField
from django.db.models.functions import Coalesce
from brands.models import Brand
from rankings.models import SearchRanking
from citations.models import AICitation
from reviews.models import Review


class DashboardOverviewView(APIView):
    """
    Dashboard overview with aggregated statistics.
    
    Optimizations applied:
    - Single aggregate queries instead of multiple count()
    - Database-level calculations
    - Prefetch for chart data
    - Limit fields with .only()
    """
    
    def get(self, request):
        # Get query params for date filtering
        start_date = request.query_params.get('start_date') or None
        end_date = request.query_params.get('end_date') or None
        
        # Single query for brand count
        total_brands = Brand.objects.count()
        
        # Build date filters once
        date_filter = Q()
        if start_date:
            date_filter &= Q(date__gte=start_date)
        if end_date:
            date_filter &= Q(date__lte=end_date)
        
        # Single aggregate query for rankings (instead of separate calls)
        rankings_stats = SearchRanking.objects.filter(date_filter).aggregate(
            avg_position=Coalesce(Avg('position'), 0.0)
        )
        
        # Single aggregate query for citations with conditional counting
        citations_stats = AICitation.objects.filter(date_filter).aggregate(
            total=Count('id'),
            mentioned=Count('id', filter=Q(mentioned=True))
        )
        total_citations = citations_stats['total']
        mentioned_citations = citations_stats['mentioned']
        citation_rate = round((mentioned_citations / total_citations) * 100, 1) if total_citations > 0 else 0
        
        # Single aggregate query for reviews
        reviews_stats = Review.objects.filter(date_filter).aggregate(
            avg_rating=Coalesce(Avg('rating'), 0.0),
            total_reviews=Coalesce(Sum('review_count'), 0)
        )
        
        return Response({
            'overview': {
                'total_brands': total_brands,
                'average_search_position': round(rankings_stats['avg_position'], 1),
                'ai_citation_rate': citation_rate,
                'average_rating': round(float(reviews_stats['avg_rating']), 1),
                'total_reviews': reviews_stats['total_reviews'],
            },
            'charts': {
                'ranking_summary': self._get_ranking_chart_data(),
                'citation_breakdown': self._get_citation_breakdown(),
                'brand_comparison': self._get_brand_comparison(),
            }
        })
    
    def _get_ranking_chart_data(self):
        """
        Get ranking data for line chart.
        Optimized: Uses prefetch_related and .only() to minimize data transfer.
        """
        # Get top 5 brands with their rankings prefetched
        brands = Brand.objects.only('id', 'name').prefetch_related(
            'rankings'
        )[:5]
        
        chart_data = []
        for brand in brands:
            # Rankings are already prefetched, no extra query needed
            # Sort in Python since prefetch doesn't support ordering well
            rankings = sorted(brand.rankings.all()[:30], key=lambda r: r.date)
            chart_data.append({
                'brand_name': brand.name,
                'data': [{'date': r.date.isoformat(), 'position': r.position} for r in rankings]
            })
        
        return chart_data
    
    def _get_citation_breakdown(self):
        """
        Get citation data for pie chart.
        Already optimized: Uses values() + annotate() for single query.
        """
        breakdown = AICitation.objects.filter(mentioned=True).values('ai_model').annotate(
            count=Count('id')
        ).order_by('-count')
        
        model_names = dict(AICitation.AI_MODEL_CHOICES)
        return [
            {'name': model_names.get(item['ai_model'], item['ai_model']), 'value': item['count']}
            for item in breakdown
        ]
    
    def _get_brand_comparison(self):
        """
        Get brand visibility scores for bar chart.
        
        OPTIMIZED: Uses database-level aggregation to calculate all stats
        in a SINGLE query instead of 4 queries per brand (N+1 problem).
        """
        # Annotate all stats at database level in ONE query
        brands = Brand.objects.annotate(
            avg_position=Coalesce(Avg('rankings__position'), 100.0),
            total_citations=Count('citations'),
            mentioned_citations=Count('citations', filter=Q(citations__mentioned=True)),
            avg_rating=Coalesce(Avg('reviews__rating'), 0.0)
        ).only('id', 'name')
        
        comparison = []
        for brand in brands:
            # All calculations done on pre-fetched annotated values (no DB calls)
            citation_rate = 0
            if brand.total_citations > 0:
                citation_rate = (brand.mentioned_citations / brand.total_citations) * 100
            
            position_score = max(0, 100 - float(brand.avg_position))
            visibility_score = (position_score * 0.4) + (citation_rate * 0.4) + (float(brand.avg_rating) * 4)
            
            comparison.append({
                'brand_name': brand.name,
                'visibility_score': round(visibility_score, 1),
                'search_score': round(position_score, 1),
                'ai_score': round(citation_rate, 1),
                'review_score': round(float(brand.avg_rating) * 20, 1)
            })
        
        return sorted(comparison, key=lambda x: x['visibility_score'], reverse=True)


class ExportDataView(APIView):
    """Export data as JSON."""
    
    def get(self, request):
        brand_id = request.query_params.get('brand')
        
        # Use .values() for lightweight dict response
        data = {
            'brands': list(Brand.objects.values('id', 'name', 'category', 'website')),
        }
        
        if brand_id:
            data['rankings'] = list(SearchRanking.objects.filter(brand_id=brand_id).values())
            data['citations'] = list(AICitation.objects.filter(brand_id=brand_id).values())
            data['reviews'] = list(Review.objects.filter(brand_id=brand_id).values())
        else:
            # Limit export to avoid memory issues
            data['rankings'] = list(SearchRanking.objects.values()[:1000])
            data['citations'] = list(AICitation.objects.values()[:1000])
            data['reviews'] = list(Review.objects.values()[:1000])
        
        return Response(data)
