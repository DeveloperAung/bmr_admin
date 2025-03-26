import logging
import traceback
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated, PermissionDenied
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status
# Set up logging
from rest_framework.views import exception_handler

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


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, (AuthenticationFailed, InvalidToken, TokenError)):
        return custom_api_response(
            success=False,
            message="Invalid credentials",
            status_code=status.HTTP_400_BAD_REQUEST
        )

    elif isinstance(exc, NotAuthenticated):
        return custom_api_response(
            success=False,
            message="Authentication required",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    elif isinstance(exc, PermissionDenied):
        return custom_api_response(
            success=False,
            message="Permission denied",
            status_code=status.HTTP_403_FORBIDDEN
        )

    if response is None:
        tb = traceback.format_exc()
        logger.error(f"Unhandled Exception: {str(exc)}\nTraceback:\n{tb}")

        return custom_api_response(
            success=False,
            message="Internal Server Error",
            errors=str(exc),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
