"""
Lightweight request logging middleware.
Only logs essential info to avoid performance impact.
"""
import logging
import time

logger = logging.getLogger('api.requests')


class RequestLoggingMiddleware:
    """
    Logs API requests with minimal overhead.
    Only logs: method, path, status, and duration.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip logging for static files and health checks
        if request.path.startswith(('/static/', '/assets/', '/favicon')):
            return self.get_response(request)
        
        start_time = time.time()
        
        response = self.get_response(request)
        
        # Calculate duration
        duration_ms = (time.time() - start_time) * 1000
        
        # Log only API requests (minimal info for speed)
        if request.path.startswith('/api/'):
            log_level = logging.WARNING if response.status_code >= 400 else logging.INFO
            logger.log(
                log_level,
                f"{request.method} {request.path} {response.status_code} {duration_ms:.0f}ms"
            )
        
        return response
