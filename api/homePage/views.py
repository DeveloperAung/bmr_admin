from rest_framework import status
from rest_framework.response import Response
from api.services import BaseSoftDeleteViewSet
from .models import HomeBanner
from .serializers import (
    HomeBannerListSerializer,
    HomeBannerRetrieveSerializer,
    HomeBannerCreateSerializer
)
import logging

logger = logging.getLogger(__name__)


class DonationSubCategoryViewSet(BaseSoftDeleteViewSet):
    queryset = HomeBanner.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return HomeBannerListSerializer
            elif self.action == "retrieve":
                return HomeBannerRetrieveSerializer
            elif self.action == "create":
                return HomeBannerCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return HomeBannerCreateSerializer
            return HomeBannerListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

