from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied, AuthenticationFailed
from rest_framework import status, viewsets
from django.utils.timezone import now
from api.custom_pagination import CustomPagination
from api.utlis import custom_api_response, url_routing_error
import logging

logger = logging.getLogger(__name__)


class BaseSoftDeleteViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet with Create, Retrieve, Update, and Soft Delete.
    """
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    def handle_authentication_error(self, request):
        """
        Returns an error response if authentication fails.
        """
        try:
            self.check_permissions(request)
            return None
        except AuthenticationFailed as e:
            # Example: Wrong username or password
            return custom_api_response(
                success=False,
                message="Invalid credentials. Please check your username and password.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        except NotAuthenticated:
            return custom_api_response(success=False, message="Authentication required",
                                       status_code=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied:
            return custom_api_response(success=False, message="Permission denied",
                                       status_code=status.HTTP_403_FORBIDDEN)

    def create(self, request, *args, **kwargs):
        auth_error = self.handle_authentication_error(request)
        if auth_error:
            return auth_error
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return custom_api_response(
                    success=True, message="Created successfully", data=serializer.data,
                    status_code=status.HTTP_201_CREATED
                )
            print()
            return custom_api_response(
                success=False, message="Validation error", errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print('create error', str(e))
            logger.error(f"Error creating object: {str(e)}")

            return custom_api_response(
                success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return custom_api_response(success=True, message="Data retrieved", data=serializer.data)
        except (NotFound, Http404):
            print('object not found')
            return custom_api_response(success=False, message="Record not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:

            error_title = type(e).__name__
            print('retrieve error', error_title)
            logger.error(f"Error retrieving object: {str(e)}")
            url_routing_error(error=error_title)
            # return custom_api_response(
            #     success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            # )

    def update(self, request, *args, **kwargs):
        auth_error = self.handle_authentication_error(request)
        if auth_error:
            return auth_error

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(modified_by=request.user)
                return custom_api_response(success=True, message="Updated successfully", data=serializer.data)
            return custom_api_response(
                success=False, message="Validation error", errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except (NotFound, Http404):
            return custom_api_response(success=False, message="Object not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('update error', str(e))
            logger.error(f"Error updating object: {str(e)}")
            return custom_api_response(
                success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        
        auth_error = self.handle_authentication_error(request)
        if auth_error:
            return auth_error

        try:
            instance = self.get_object()
            if not instance.is_active:
                return custom_api_response(
                    success=False, message="Record already deleted", status_code=status.HTTP_400_BAD_REQUEST
                )

            instance.is_active = False
            instance.deleted_at = now()
            instance.deleted_by = request.user
            instance.save()

            return custom_api_response(success=True, message="Record deleted successfully")
        except (NotFound, Http404):
            return custom_api_response(success=False, message="Object not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('update error', str(e))
            logger.error(f"Error updating object: {str(e)}")
            return custom_api_response(
                success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


