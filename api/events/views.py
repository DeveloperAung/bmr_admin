import logging

from rest_framework.decorators import action
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import APIException
from drf_spectacular.utils import extend_schema_view, extend_schema
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
from ..services import BaseSoftDeleteViewSet
from ..utlis import url_routing_error, custom_api_response
from django.utils import timezone

logger = logging.getLogger(__name__)


@extend_schema(tags=["Event Category"])
class EventCategoryViewSet(BaseSoftDeleteViewSet):
    def get_queryset(self):
        queryset = EventCategory.objects.filter(is_active=True).order_by('title')
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
            )
        return queryset

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
            # error_title = type(e).__name__
            # raise APIException(detail=f"Serializer selection failed: {error_title}")
            url_routing_error(error=e)


@extend_schema(tags=["Event Sub Category"])
class EventSubCategoryViewSet(BaseSoftDeleteViewSet):
    def get_queryset(self):
        queryset = EventSubCategory.objects.filter(is_active=True).order_by('title')
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(event_category__title__icontains=search)
            )
        return queryset

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
            url_routing_error(error=e)


@extend_schema(tags=["Event"])
class EventViewSet(BaseSoftDeleteViewSet):

    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True).order_by('-created_at')
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(short_description__icontains=search) |
                Q(category__title__icontains=search) |
                Q(short_description__icontains=search)
            )
        return queryset

    def get_serializer_class(self):
        """Returns different serializer based on action"""
        try:
            if self.action == "list":
                return EventListSerializer
            elif self.action == "retrieve":
                return EventRetrieveSerializer
            elif self.action == "create":
                return EventCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return EventUpdateSerializer
            return EventRetrieveSerializer
        except Exception as e:
            url_routing_error(error=e)

    @action(detail=True, methods=["patch"], url_path="publish-toggle")
    def publish_toggle(self, request, uuid=None):
        try:
            event = self.get_object()
            try:
                is_published = False if event.is_publish else True
                event.is_publish = is_published

                if is_published:
                    event.published_by = request.user
                    event.published_at = timezone.now()
                event.save()
                return custom_api_response(
                    success=True,
                    message=f"Event {'published' if is_published else 'unpublished'} successfully",
                    data={
                        "id": event.id,
                        "is_published": event.is_publish,
                        "published_by": event.published_by.id if event.published_by else None,
                        "published_at": event.published_at,
                    }
                )
                # return notice.get(uuid=uuid)
            except event.DoesNotExist:
                return custom_api_response(
                    success=False,
                    message="Record not exists",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            error_title = type(e).__name__
            print("publish_toggle error:", error_title)
            logger.error(f"Error toggling publish status: {error_title}")
            return custom_api_response(
                success=False,
                message=error_title,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

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


@extend_schema(tags=["Event Date"])
class EventDateViewSet(BaseSoftDeleteViewSet):
    queryset = EventDate.objects.all()
    serializer_class = EventDateSerializer
