from rest_framework.views import exception_handler
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework import status
import logging
logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, IntegrityError):
        # Log a concise error message without the full traceback
        logger.error(f"IntegrityError: {str(exc)}")
        return Response(
            {"error": "A database integrity error occurred. Please check your data."},
            status=status.HTTP_400_BAD_REQUEST
        )

    return response
