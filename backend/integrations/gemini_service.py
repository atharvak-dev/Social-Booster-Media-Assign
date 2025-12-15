"""
Gemini API integration service for AI citation checking.
Uses Google's Gemini API to check if brands are mentioned in AI responses.
Includes semantic detection to verify if responses describe the brand.
"""
import time
import requests
from django.conf import settings


class GeminiService:
    """Service for interacting with Google's Gemini API."""
    
    BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'
    MAX_RETRIES = 3
    INITIAL_BACKOFF = 5  # seconds
    
    def __init__(self):
        self.api_key = getattr(settings, 'GEMINI_API_KEY', '')
    
    def _make_request(self, json_data: dict, timeout: int = 30) -> requests.Response:
        """Make API request with retry logic for rate limiting."""
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.post(
                    f"{self.BASE_URL}?key={self.api_key}",
                    headers={'Content-Type': 'application/json'},
                    json=json_data,
                    timeout=timeout
                )
                
                if response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = self.INITIAL_BACKOFF * (2 ** attempt)
                    time.sleep(wait_time)
                    continue
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise
                time.sleep(self.INITIAL_BACKOFF * (2 ** attempt))
        
        return response
    
    def _extract_response_text(self, data: dict) -> str:
        """Extract text from Gemini API response."""
        response_text = ''
        if 'candidates' in data and len(data['candidates']) > 0:
            candidate = data['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                for part in candidate['content']['parts']:
                    if 'text' in part:
                        response_text += part['text']
        return response_text
    
    def _semantic_verify(self, brand_name: str, response_text: str) -> bool:
        """
        Use Gemini to semantically verify if the response describes the brand.
        This handles cases where the brand name isn't explicitly mentioned.
        """
        if not response_text or len(response_text) < 20:
            return False
        
        try:
            verify_prompt = f"""Analyze this text and answer only YES or NO:
Does this text describe or discuss "{brand_name}" (the company/product)?

Text to analyze:
{response_text[:800]}

Answer only YES or NO:"""
            
            response = self._make_request({
                'contents': [{'parts': [{'text': verify_prompt}]}],
                'generationConfig': {
                    'temperature': 0.1,
                    'maxOutputTokens': 10,
                }
            }, timeout=15)
            
            verify_text = self._extract_response_text(response.json()).strip().upper()
            return 'YES' in verify_text
            
        except Exception:
            return False
    
    def check_brand_citation(self, brand_name: str, query: str) -> dict:
        """
        Check if a brand is mentioned when asking Gemini a question.
        Uses semantic detection to verify even when brand name isn't explicit.
        
        Args:
            brand_name: Name of the brand to look for
            query: Question to ask Gemini
            
        Returns:
            dict with citation result
        """
        if not self.api_key:
            return {'error': 'Gemini API key not configured', 'mentioned': False}
        
        try:
            response = self._make_request({
                'contents': [{'parts': [{'text': query}]}],
                'generationConfig': {
                    'temperature': 0.7,
                    'maxOutputTokens': 1024,
                }
            })
            data = response.json()
            response_text = self._extract_response_text(data)
            
            # First check: direct mention (case-insensitive)
            brand_lower = brand_name.lower()
            response_lower = response_text.lower()
            direct_mention = brand_lower in response_lower
            
            # Second check: semantic verification if no direct mention
            mentioned = direct_mention
            if not direct_mention and response_text:
                mentioned = self._semantic_verify(brand_name, response_text)
            
            # Extract context
            context = ''
            if direct_mention:
                pos = response_lower.find(brand_lower)
                start = max(0, pos - 100)
                end = min(len(response_text), pos + len(brand_name) + 100)
                context = response_text[start:end]
                if start > 0:
                    context = '...' + context
                if end < len(response_text):
                    context = context + '...'
            elif mentioned:
                # Semantic match - use first part of response as context
                context = response_text[:200] + '...' if len(response_text) > 200 else response_text
            
            return {
                'mentioned': mentioned,
                'direct_mention': direct_mention,
                'semantic_match': mentioned and not direct_mention,
                'citation_context': context if mentioned else 'Brand not described in response',
                'full_response': response_text[:500] if response_text else '',
                'success': True
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'error': str(e),
                'mentioned': False,
                'citation_context': f'API error: {str(e)}',
                'success': False
            }
    
    def test_connection(self) -> dict:
        """Test the Gemini API connection."""
        if not self.api_key:
            return {'success': False, 'error': 'Gemini API key not configured'}
        
        try:
            response = self._make_request({
                'contents': [{'parts': [{'text': 'Say OK'}]}],
                'generationConfig': {'maxOutputTokens': 10}
            }, timeout=15)
            return {'success': True, 'message': 'Gemini API connection successful'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': str(e)}
