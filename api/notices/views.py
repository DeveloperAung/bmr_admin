from rest_framework import status
from rest_framework.response import Response
from api.services import BaseSoftDeleteViewSet
from .models import Notice
from .serializers import (
    NoticeListSerializer,
    NoticeRetrieveSerializer,
    NoticeCreateSerializer
)
import logging

logger = logging.getLogger(__name__)


class NoticeViewSet(BaseSoftDeleteViewSet):
    queryset = Notice.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return NoticeListSerializer
            elif self.action == "retrieve":
                return NoticeRetrieveSerializer
            elif self.action == "create":
                return NoticeCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return NoticeCreateSerializer
            return NoticeListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": f"Internal Server Error {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

