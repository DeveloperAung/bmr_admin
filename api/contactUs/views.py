from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import ContactUs
from .serializers import ContactUsUserSerializer, ContactUsAdminSerializer
from ..custom_pagination import CustomPagination
from ..utlis import custom_api_response
import logging

# Set up logging
logger = logging.getLogger(__name__)


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.filter(is_active=True).order_by("-created_at")
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]  # ✅ Use JWT for authentication
    permission_classes = [IsAuthenticated]  # ✅ Only authenticated users can access
    lookup_field = "uuid"

    def get_permissions(self):
        """Assign permissions based on the action."""
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]  # ✅ Require authentication for GET requests
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAdminUser()]  # ✅ Admins can update or delete
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Return the appropriate serializer based on the user role."""
        if self.request.user.is_staff:  # Admin users
            return ContactUsAdminSerializer
        return ContactUsUserSerializer  # Regular users

    def list(self, request, *args, **kwargs):
        """Handle GET request to list all contact messages with pagination."""
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)  # Apply pagination
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)  # Use paginated response

            serializer = self.get_serializer(queryset, many=True)
            return custom_api_response(success=True, message="Contact messages retrieved successfully.", data=serializer.data)
        except Exception as e:
            logger.error(f"Error in list view: {str(e)}", exc_info=True)
            return custom_api_response(success=False, message="Failed to retrieve contact messages.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        """Handle GET request to retrieve a single contact message using UUID."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return custom_api_response(success=True, message="Contact message retrieved successfully.",
                                       data=serializer.data)
        except NotFound:
            return custom_api_response(success=False, message="Message not found.",
                                       status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in retrieve view: {str(e)}", exc_info=True)
            return custom_api_response(success=False, message="Failed to retrieve message.",
                                       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """User submits a contact request."""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return custom_api_response(success=True, message="Message submitted successfully.", data=serializer.data,
                                       status_code=status.HTTP_201_CREATED)
        except ValidationError as e:
            logger.warning(f"Validation error in create view: {str(e)}")
            return custom_api_response(success=False, message="Invalid data provided.", data=e.detail, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in create view: {str(e)}", exc_info=True)
            return custom_api_response(success=False, message="Failed to submit contact message.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        """Admin replies to a message."""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True, context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return custom_api_response(success=True, message="Reply sent successfully.", data=serializer.data)
        except ValidationError as e:
            logger.warning(f"Validation error in update view: {str(e)}")
            return custom_api_response(success=False, message="Invalid data provided.", data=e.detail, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error in update view: {str(e)}", exc_info=True)
            return custom_api_response(success=False, message="Failed to update contact message.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        """Perform soft delete instead of hard delete"""
        try:
            instance = self.get_object()
            instance.soft_delete(request.user)
            return custom_api_response(success=True, message="Contact message soft-deleted successfully.")
        except Exception as e:
            logger.error(f"Error in soft delete: {str(e)}", exc_info=True)
            return custom_api_response(success=False, message="Failed to delete contact message.",
                                       status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)



