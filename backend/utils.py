"""
Utility functions and custom exception handlers.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that provides consistent error responses.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data
        custom_response_data = {
            "success": False,
            "error": {"message": str(exc), "details": response.data},
        }
        response.data = custom_response_data
    else:
        # Handle unexpected exceptions
        logger.error(f"Unexpected error: {exc}", exc_info=True)
        custom_response_data = {
            "success": False,
            "error": {"message": "An unexpected error occurred.", "details": str(exc)},
        }
        response = Response(
            custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Standardized success response format.
    """
    return Response(
        {"success": True, "message": message, "data": data}, status=status_code
    )


def error_response(
    message="Error", details=None, status_code=status.HTTP_400_BAD_REQUEST
):
    """
    Standardized error response format.
    """
    return Response(
        {"success": False, "error": {"message": message, "details": details}},
        status=status_code,
    )
