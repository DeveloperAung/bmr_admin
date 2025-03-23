from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.services import BaseSoftDeleteViewSet
from django.utils import timezone
from .models import PostCategory, Post
from .serializers import (
    PostCategoryListSerializer,
    PostCategoryCreateSerializer,
    PostCategoryRetrieveSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
    PostCreateSerializer
)
import logging

from ..utlis import custom_api_response

logger = logging.getLogger(__name__)


@extend_schema(tags=["Post Category"])
class PostCategoryViewSet(BaseSoftDeleteViewSet):
    queryset = PostCategory.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return PostCategoryListSerializer
            elif self.action == "retrieve":
                return PostCategoryRetrieveSerializer
            elif self.action == "create":
                return PostCategoryCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return PostCategoryCreateSerializer
            return PostCategoryListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=["Post"])
class PostViewSet(BaseSoftDeleteViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    queryset = Post.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return PostListSerializer
            elif self.action == "retrieve":
                return PostRetrieveSerializer
            elif self.action == "create":
                return PostCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return PostCreateSerializer
            return PostListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=["patch"], url_path="publish-toggle")
    def publish_toggle(self, request, uuid=None):
        try:
            post = self.get_object()
            try:
                is_published = False if post.is_published else True
                post.is_published = is_published

                if is_published:
                    post.published_by = request.user
                    post.published_at = timezone.now()
                post.save()
                return custom_api_response(
                    success=True,
                    message=f"Notice {'published' if is_published else 'unpublished'} successfully",
                    data={
                        "id": post.id,
                        "is_published": post.is_published,
                        "published_by": post.published_by.id if post.published_by else None,
                        "published_at": post.published_at,
                    }
                )
            except Post.DoesNotExist:
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