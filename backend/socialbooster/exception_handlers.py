"""
Custom exception handler for consistent API error responses.
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent JSON error format.
    
    Response format:
    {
        "error": true,
        "code": "ERROR_CODE",
        "message": "Human readable message",
        "details": {}
    }
    """
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)
    
    if response is not None:
        # Map status codes to error codes
        error_codes = {
            400: 'BAD_REQUEST',
            401: 'UNAUTHORIZED',
            403: 'FORBIDDEN',
            404: 'NOT_FOUND',
            405: 'METHOD_NOT_ALLOWED',
            429: 'RATE_LIMIT_EXCEEDED',
            500: 'INTERNAL_ERROR',
        }
        
        error_code = error_codes.get(response.status_code, 'ERROR')
        
        # Get the error message
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                message = str(response.data['detail'])
                details = {}
            else:
                message = 'Validation error'
                details = response.data
        elif isinstance(response.data, list):
            message = response.data[0] if response.data else 'Error'
            details = {'errors': response.data}
        else:
            message = str(response.data)
            details = {}
        
        # Log the error
        logger.warning(
            f"API Error: {error_code} - {message}",
            extra={
                'status_code': response.status_code,
                'path': context['request'].path if context.get('request') else None,
            }
        )
        
        response.data = {
            'error': True,
            'code': error_code,
            'message': message,
            'details': details,
        }
    
    return response
