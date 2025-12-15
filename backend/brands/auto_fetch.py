"""
Auto-fetch service for new brands.
Automatically fetches real data from the internet when a brand is created.
"""
from datetime import date
from integrations.services import SerpAPIService
from rankings.models import SearchRanking
from citations.models import AICitation
from reviews.models import Review


# Category to keyword mapping for generating relevant search terms
CATEGORY_KEYWORDS = {
    'software': ['software', 'app', 'tool', 'solution'],
    'ecommerce': ['online store', 'shop', 'marketplace', 'retail'],
    'finance': ['finance', 'accounting', 'bookkeeping', 'financial'],
    'health': ['health', 'wellness', 'medical', 'healthcare'],
    'food': ['food', 'restaurant', 'delivery', 'cuisine'],
    'services': ['services', 'consulting', 'agency', 'professional'],
    'other': ['company', 'business', 'brand'],
}


def generate_keywords(brand_name: str, category: str) -> list:
    """
    Generate search keywords based on brand name and category.
    
    Args:
        brand_name: Name of the brand
        category: Category of the brand
        
    Returns:
        List of keywords to search for
    """
    keywords = []
    
    # Add brand name as a keyword
    keywords.append(brand_name)
    
    # Get category-specific keywords
    category_terms = CATEGORY_KEYWORDS.get(category, CATEGORY_KEYWORDS['other'])
    
    # Combine brand name with category terms
    for term in category_terms[:2]:  # Limit to 2 category terms to save API credits
        keywords.append(f"{brand_name} {term}")
    
    # Add "best" query for competitive analysis
    if category_terms:
        keywords.append(f"best {category_terms[0]}")
    
    return keywords


def auto_fetch_rankings(brand):
    """
    Fetch real Google search rankings for a brand.
    
    Args:
        brand: Brand model instance
        
    Returns:
        dict with results summary
    """
    service = SerpAPIService()
    keywords = generate_keywords(brand.name, brand.category)
    results = []
    
    for keyword in keywords:
        try:
            result = service.check_brand_position(brand.name, keyword)
            
            if result.get('found') and result.get('position'):
                # Save the ranking
                SearchRanking.objects.update_or_create(
                    brand=brand,
                    keyword=keyword,
                    date=date.today(),
                    defaults={'position': result['position']}
                )
                results.append({
                    'keyword': keyword,
                    'position': result['position'],
                    'success': True
                })
            else:
                # Brand not found in top results, save with high position
                SearchRanking.objects.update_or_create(
                    brand=brand,
                    keyword=keyword,
                    date=date.today(),
                    defaults={'position': 100}  # Not in top 100
                )
                results.append({
                    'keyword': keyword,
                    'position': None,
                    'success': True,
                    'note': 'Brand not found in top 100 results'
                })
        except Exception as e:
            results.append({
                'keyword': keyword,
                'success': False,
                'error': str(e)
            })
    
    return {
        'rankings_fetched': len([r for r in results if r.get('success')]),
        'total_keywords': len(keywords),
        'results': results
    }


def auto_fetch_citations(brand):
    """
    Fetch real AI citations for a brand using Gemini API.
    
    Args:
        brand: Brand model instance
        
    Returns:
        dict with results summary
    """
    from integrations.gemini_service import GeminiService
    
    gemini_service = GeminiService()
    
    # Query templates to check if the brand is mentioned
    query_templates = [
        f"What is {brand.name}?",
        f"Tell me about {brand.name}",
    ]
    
    citations_created = 0
    mentions_found = 0
    
    for query in query_templates:
        try:
            # Check with Gemini API
            result = gemini_service.check_brand_citation(brand.name, query)
            
            mentioned = result.get('mentioned', False)
            context = result.get('citation_context', 'Unable to check')
            
            if mentioned:
                mentions_found += 1
            
            # Save the citation result for Gemini
            AICitation.objects.update_or_create(
                brand=brand,
                ai_model='gemini',
                query=query,
                date=date.today(),
                defaults={
                    'mentioned': mentioned,
                    'citation_context': context
                }
            )
            citations_created += 1
            
        except Exception as e:
            # Create a placeholder entry on error
            AICitation.objects.update_or_create(
                brand=brand,
                ai_model='gemini',
                query=query,
                date=date.today(),
                defaults={
                    'mentioned': False,
                    'citation_context': f'Error checking: {str(e)}'
                }
            )
            citations_created += 1
    
    # Create placeholder entries for other AI models (not implemented yet)
    other_models = ['chatgpt', 'perplexity']
    for ai_model in other_models:
        for query in query_templates:
            AICitation.objects.get_or_create(
                brand=brand,
                ai_model=ai_model,
                query=query,
                date=date.today(),
                defaults={
                    'mentioned': False,
                    'citation_context': f'Pending - {ai_model.upper()} API not configured'
                }
            )
            citations_created += 1
    
    return {
        'citations_created': citations_created,
        'mentions_found': mentions_found,
        'ai_models_checked': ['gemini'],
        'pending_models': other_models
    }


def auto_fetch_reviews(brand):
    """
    Create initial review entries for a brand.
    
    Args:
        brand: Brand model instance
        
    Returns:
        dict with results summary
    """
    platforms = ['google', 'trustpilot', 'g2']
    reviews_created = 0
    
    for platform in platforms:
        Review.objects.get_or_create(
            brand=brand,
            platform=platform,
            date=date.today(),
            defaults={
                'rating': 0.0,  # Will be updated when actually scraped
                'review_count': 0
            }
        )
        reviews_created += 1
    
    return {
        'reviews_created': reviews_created,
        'platforms_added': len(platforms)
    }


def auto_fetch_brand_data(brand):
    """
    Orchestrate all data fetching for a new brand.
    
    Args:
        brand: Brand model instance
        
    Returns:
        dict with all results
    """
    results = {
        'brand_id': brand.id,
        'brand_name': brand.name,
        'rankings': auto_fetch_rankings(brand),
        'citations': auto_fetch_citations(brand),
        'reviews': auto_fetch_reviews(brand),
    }
    
    return results
