from rest_framework import status
from rest_framework.response import Response
from api.services import BaseSoftDeleteViewSet
from .models import PostCategory
from .serializers import (
    PostCategoryListSerializer,
    PostCategoryCreateSerializer,
    PostCategoryRetrieveSerializer
)
import logging

logger = logging.getLogger(__name__)


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
