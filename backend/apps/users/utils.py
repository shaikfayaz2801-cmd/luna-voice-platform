"""
Shared utility functions for the Luna AI Platform.
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom DRF exception handler that returns consistent error responses.
    Format: { "error": "...", "detail": "...", "code": "..." }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'error': True,
            'status_code': response.status_code,
        }

        if isinstance(response.data, dict):
            if 'detail' in response.data:
                error_data['detail'] = str(response.data['detail'])
                error_data['code'] = getattr(response.data.get('detail'), 'code', 'error')
            else:
                error_data['detail'] = response.data
        elif isinstance(response.data, list):
            error_data['detail'] = response.data
        else:
            error_data['detail'] = str(response.data)

        response.data = error_data

    return response


def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')
