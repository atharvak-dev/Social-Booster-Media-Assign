"""
SerpAPI integration service.
Uses SerpAPI for reliable Google search results.
"""
import requests
from django.conf import settings
from datetime import date


class SerpAPIService:
    """Service for interacting with SerpAPI for Google Search."""
    
    BASE_URL = 'https://serpapi.com/search'
    
    def __init__(self):
        self.api_key = getattr(settings, 'SERPAPI_KEY', '')
    
    def search_google(self, query: str, num_results: int = 10) -> dict:
        """
        Search Google and return organic results.
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            dict with search results
        """
        if not self.api_key:
            return {'error': 'SerpAPI key not configured'}
        
        try:
            response = requests.get(
                self.BASE_URL,
                params={
                    'api_key': self.api_key,
                    'engine': 'google',
                    'q': query,
                    'num': num_results,
                    'hl': 'en',
                    'gl': 'us'
                },
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            # Extract organic results
            organic_results = data.get('organic_results', [])
            results = []
            
            for r in organic_results[:num_results]:
                results.append({
                    'title': r.get('title', ''),
                    'link': r.get('link', ''),
                    'snippet': r.get('snippet', ''),
                    'position': r.get('position', 0)
                })
            
            return {'results': results}
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def check_brand_position(self, brand_name: str, keyword: str) -> dict:
        """
        Check a brand's position in Google search results for a keyword.
        
        Args:
            brand_name: Name of the brand to look for
            keyword: Search keyword
            
        Returns:
            dict with position and search results
        """
        results = self.search_google(keyword, num_results=100)
        
        if 'error' in results:
            return results
        
        position = None
        search_results = results.get('results', [])
        
        brand_lower = brand_name.lower()
        
        for idx, result in enumerate(search_results, start=1):
            title = result.get('title', '').lower()
            link = result.get('link', '').lower()
            snippet = result.get('snippet', '').lower()
            
            # Check if brand name appears in title, link, or snippet
            if brand_lower in title or brand_lower in link or brand_lower in snippet:
                position = idx
                break
        
        return {
            'keyword': keyword,
            'brand': brand_name,
            'position': position,
            'found': position is not None,
            'date': date.today().isoformat(),
            'total_results_checked': len(search_results)
        }
    
    def get_api_usage(self) -> dict:
        """Check SerpAPI account info."""
        if not self.api_key:
            return {'error': 'SerpAPI key not configured'}
        
        try:
            response = requests.get(
                'https://serpapi.com/account',
                params={'api_key': self.api_key},
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
