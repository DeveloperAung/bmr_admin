import logging

from rest_framework.response import Response
from rest_framework import status
# Set up logging
logger = logging.getLogger(__name__)


def custom_api_response(success=True, message="", errors=None, data=None, status_code=status.HTTP_200_OK):
    """
    Standardized API response format.
    """
    response_data = {
        "success": success,
        "message": message,
        "errors": errors if errors else None,
        "data": data if data else {}
    }

    # Log errors for debugging
    if not success:
        logger.error(f"API Error: {message}")

    return Response(response_data, status=status_code, content_type="application/json; charset=utf-8")


def url_routing_error(error=None):
    print('error', error)
    logger.error(f"Error selecting serializer: {error}")
    return custom_api_response(
        success=False,
        message="Internal Server Error",
        errors=error,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )



