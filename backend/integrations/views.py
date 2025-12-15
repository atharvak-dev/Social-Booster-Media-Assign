from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date
from .services import SerpAPIService
from brands.models import Brand
from rankings.models import SearchRanking


class SearchBrandRankingView(APIView):
    """Search Google for brand ranking data using SerpAPI."""
    
    def post(self, request):
        """
        Search Google for brand position.
        
        Request body:
        {
            "brand_id": 1,
            "keyword": "accounting software"
        }
        """
        brand_id = request.data.get('brand_id')
        keyword = request.data.get('keyword')
        
        if not brand_id or not keyword:
            return Response(
                {'error': 'brand_id and keyword are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response(
                {'error': f'Brand with id {brand_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        service = SerpAPIService()
        result = service.check_brand_position(brand.name, keyword)
        
        if 'error' in result:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Save the ranking if found
        if result['found']:
            SearchRanking.objects.update_or_create(
                brand=brand,
                keyword=keyword,
                date=date.today(),
                defaults={'position': result['position']}
            )
        
        return Response(result)


class APIUsageView(APIView):
    """Check SerpAPI usage."""
    
    def get(self, request):
        service = SerpAPIService()
        usage = service.get_api_usage()
        return Response(usage)


class BulkSearchView(APIView):
    """Bulk search rankings for all brands with their keywords."""
    
    def post(self, request):
        """
        Search rankings for multiple brands/keywords.
        
        Request body:
        {
            "queries": [
                {"brand_id": 1, "keyword": "accounting software"},
                {"brand_id": 2, "keyword": "cloud storage"}
            ]
        }
        """
        queries = request.data.get('queries', [])
        
        if not queries:
            return Response(
                {'error': 'queries array is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        service = SerpAPIService()
        results = []
        
        for query in queries:
            brand_id = query.get('brand_id')
            keyword = query.get('keyword')
            
            if not brand_id or not keyword:
                results.append({'error': 'brand_id and keyword required', 'query': query})
                continue
            
            try:
                brand = Brand.objects.get(id=brand_id)
                result = service.check_brand_position(brand.name, keyword)
                
                if result.get('found'):
                    SearchRanking.objects.update_or_create(
                        brand=brand,
                        keyword=keyword,
                        date=date.today(),
                        defaults={'position': result['position']}
                    )
                
                results.append(result)
            except Brand.DoesNotExist:
                results.append({'error': f'Brand {brand_id} not found', 'query': query})
        
        return Response({
            'total': len(queries),
            'results': results
        })


class GeminiTestView(APIView):
    """Test Gemini API connection."""
    
    def get(self, request):
        from .gemini_service import GeminiService
        service = GeminiService()
        result = service.test_connection()
        
        if result['success']:
            return Response(result)
        return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GeminiCitationCheckView(APIView):
    """Check brand citation using Gemini API."""
    
    def post(self, request):
        """
        Check if a brand is mentioned by Gemini.
        
        Request body:
        {
            "brand_id": 1,
            "query": "What is the best accounting software?"
        }
        """
        from .gemini_service import GeminiService
        from citations.models import AICitation
        
        brand_id = request.data.get('brand_id')
        query = request.data.get('query')
        
        if not brand_id or not query:
            return Response(
                {'error': 'brand_id and query are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            return Response(
                {'error': f'Brand with id {brand_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        service = GeminiService()
        result = service.check_brand_citation(brand.name, query)
        
        if result.get('success'):
            # Save the citation result
            AICitation.objects.update_or_create(
                brand=brand,
                ai_model='gemini',
                query=query,
                date=date.today(),
                defaults={
                    'mentioned': result['mentioned'],
                    'citation_context': result['citation_context']
                }
            )
        
        return Response({
            'brand': brand.name,
            'query': query,
            'mentioned': result.get('mentioned', False),
            'context': result.get('citation_context', ''),
            'full_response': result.get('full_response', '')[:500]
        })
