import logging
from rest_framework.response import Response
from rest_framework import status


# Set up logging
logger = logging.getLogger(__name__)


def custom_api_response(success=True, message="", data=None, status_code=status.HTTP_200_OK):
    """
    Standardized API response format.
    """
    response_data = {
        "success": success,
        "message": message,
        "data": data if data else {}
    }

    # Log errors for debugging
    if not success:
        logger.error(f"API Error: {message}")

    return Response(response_data, status=status_code)
