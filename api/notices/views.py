from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema_view, extend_schema

from api.services import BaseSoftDeleteViewSet
from .models import Notice
from .serializers import (
    NoticeListSerializer,
    NoticeRetrieveSerializer,
    NoticeCreateSerializer
)
import logging

from ..utlis import custom_api_response

logger = logging.getLogger(__name__)


@extend_schema(tags=["Notice"])
class NoticeViewSet(BaseSoftDeleteViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_serializer_class(self):
        if self.action == "list":
            return NoticeListSerializer
        elif self.action == "retrieve":
            return NoticeRetrieveSerializer
        elif self.action == "create":
            return NoticeCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return NoticeCreateSerializer
        return NoticeRetrieveSerializer

    def get_queryset(self):
        queryset = Notice.objects.filter(is_active=True).order_by('-created_at')
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

    @action(detail=True, methods=["patch"], url_path="publish-toggle")
    def publish_toggle(self, request, uuid=None):
        try:
            notice = self.get_object()
            # uuid = self.kwargs.get(self.lookup_field)
            try:
                # is_published = request.data.get("is_published")

                # if is_published is None:
                #     return custom_api_response(
                #         success=False,
                #         message="Missing 'is_published' in request body",
                #         status_code=status.HTTP_400_BAD_REQUEST,
                #     )

                is_published = False if notice.is_published else True
                notice.is_published = is_published

                if is_published:
                    notice.published_by = request.user
                    notice.published_at = timezone.now()
                notice.save()
                return custom_api_response(
                    success=True,
                    message=f"Notice {'published' if is_published else 'unpublished'} successfully",
                    data={
                        "id": notice.id,
                        "is_published": notice.is_published,
                        "published_by": notice.published_by.id if notice.published_by else None,
                        "published_at": notice.published_at,
                    }
                )
                # return notice.get(uuid=uuid)
            except Notice.DoesNotExist:
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

