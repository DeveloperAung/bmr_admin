import logging
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import EventCategory, EventSubCategory, Event, EventDate
from .serializers import EventDateSerializer
from .serializers import (
    EventCategoryListSerializer,
    EventCategoryRetrieveSerializer,
    EventCategoryCreateSerializer
)
from .serializers import (
    EventSubCategoryListSerializer,
    EventSubCategoryRetrieveSerializer,
    EventSubCategoryCreateSerializer
)
from .serializers import (
    EventListSerializer,
    EventRetrieveSerializer,
    EventCreateSerializer,
    EventUpdateSerializer,
)
from ..custom_pagination import CustomPagination
from ..utlis import custom_api_response

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
                return custom_api_response(success=True, message="Created successfully", data=serializer.data)
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
        except NotFound:
            return custom_api_response(success=False, message="Object not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('retrieve error', e)
            logger.error(f"Error retrieving object: {str(e)}")
            return custom_api_response(
                success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
        except NotFound:
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

        instance = self.get_object()
        if not instance.is_active:
            return custom_api_response(
                success=False, message="Item already deleted", status_code=status.HTTP_400_BAD_REQUEST
            )

        instance.is_active = False
        instance.deleted_at = now()
        instance.deleted_by = request.user
        instance.save()

        return custom_api_response(success=True, message="Item deleted successfully")


class EventCategoryViewSet(BaseSoftDeleteViewSet):
    queryset = EventCategory.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return EventCategoryListSerializer
            elif self.action == "retrieve":
                return EventCategoryRetrieveSerializer
            elif self.action == "create":
                return EventCategoryCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return EventCategoryCreateSerializer
            return EventCategoryListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventSubCategoryViewSet(BaseSoftDeleteViewSet):
    queryset = EventSubCategory.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return EventSubCategoryListSerializer
            elif self.action == "retrieve":
                return EventSubCategoryRetrieveSerializer
            elif self.action == "create":
                return EventSubCategoryCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return EventSubCategoryCreateSerializer
            return EventSubCategoryListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EventViewSet(BaseSoftDeleteViewSet):
    queryset = Event.objects.filter(is_active=True).order_by('-created_at')

    def get_serializer_class(self):
        """Returns different serializer based on action"""
        if self.action == "list":
            return EventListSerializer
        elif self.action == "retrieve":
            print('event list')
            return EventRetrieveSerializer
        elif self.action == "create":
            return EventCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return EventUpdateSerializer
        return EventRetrieveSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     """
    #     Handle nested event dates when creating an event.
    #     """
    #     auth_error = self.handle_authentication_error(request)
    #     if auth_error:
    #         return auth_error
    #     try:
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance)
    #         return custom_api_response(success=True, message="Event retrieved successfully.",
    #                                    data=serializer.data)
    #     except NotFound:
    #         return custom_api_response(success=False, message="Event not found.",
    #                                    status_code=status.HTTP_404_NOT_FOUND)
    #     except Exception as e:
    #         logger.error(f"Error in event retrieve view: {str(e)}", exc_info=True)
    #         return custom_api_response(success=False, message="Failed to retrieve event.",
    #                                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    #
    # def create(self, request, *args, **kwargs):
    #     """
    #     Handle nested event dates when creating an event.
    #     """
    #     auth_error = self.handle_authentication_error(request)
    #     if auth_error:
    #         return auth_error
    #
    #     try:
    #         serializer = self.get_serializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save(created_by=request.user)
    #             return custom_api_response(success=True, message="Event created successfully", data=serializer.data)
    #         return custom_api_response(
    #             success=False, message="Validation error", errors=serializer.errors,
    #             status_code=status.HTTP_400_BAD_REQUEST
    #         )
    #     except Exception as e:
    #         logger.error(f"Error creating Event: {str(e)}")
    #         return custom_api_response(
    #             success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )
    #
    # def update(self, request, *args, **kwargs):
    #     """
    #     Handle nested event dates when updating an event.
    #     """
    #     auth_error = self.handle_authentication_error(request)
    #     if auth_error:
    #         return auth_error
    #
    #     try:
    #         instance = self.get_object()
    #         serializer = self.get_serializer(instance, data=request.data, partial=True)
    #         if serializer.is_valid():
    #             serializer.save(modified_by=request.user)
    #             return custom_api_response(success=True, message="Event updated successfully", data=serializer.data)
    #         return custom_api_response(
    #             success=False, message="Validation error", errors=serializer.errors,
    #             status_code=status.HTTP_400_BAD_REQUEST
    #         )
    #     except Exception as e:
    #         logger.error(f"Error updating Event: {str(e)}")
    #         return custom_api_response(
    #             success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )


class EventDateViewSet(BaseSoftDeleteViewSet):
    queryset = EventDate.objects.all()
    serializer_class = EventDateSerializer
