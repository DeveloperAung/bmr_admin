from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from api.services import BaseSoftDeleteViewSet
from .models import SinglePage
from .serializers import (
    SinglePageListSerializer,
    SinglePageRetrieveSerializer,
    SinglePageCreateSerializer
)
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=["Single Page"])
class SinglePageViewSet(BaseSoftDeleteViewSet):
    queryset = SinglePage.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return SinglePageListSerializer
            elif self.action == "retrieve":
                return SinglePageRetrieveSerializer
            elif self.action == "create":
                return SinglePageCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return SinglePageCreateSerializer
            return SinglePageListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

