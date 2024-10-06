from rest_framework.views import exception_handler
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
import logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    request = context.get('request')
    user = request.user if request else 'Unknown User'
    path = request.path if request else 'Unknown Path'
    method = request.method if request else 'Unknown Method'

    if isinstance(exc, IntegrityError):
        logger.error(
            f"IntegrityError: {str(exc)} | User: {user} | Path: {path} | Method: {method}"
        )
        return Response(
            {"error": "A database integrity error occurred. Please check your data."},
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        logger.error(
            f"Error: {str(exc)} | User: {user} | Path: {path} | Method: {method}"
        )

    return response
