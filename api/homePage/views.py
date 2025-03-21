from rest_framework import status
from rest_framework.decorators import action

from api.services import BaseSoftDeleteViewSet
from .models import HomeBanner
from .serializers import (
    HomeBannerListSerializer,
    HomeBannerRetrieveSerializer,
    HomeBannerCreateSerializer,
    HomeBannerReorderSerializer
)
import logging
from ..utlis import url_routing_error, custom_api_response

logger = logging.getLogger(__name__)


class HomeBannerViewSet(BaseSoftDeleteViewSet):
    queryset = HomeBanner.objects.all().order_by('order_index')

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
            elif self.action == "reorder":
                return HomeBannerReorderSerializer
            return HomeBannerListSerializer
        except Exception as e:
            url_routing_error(error=e)

    @action(detail=False, methods=['post'], url_path='update-order')
    def reorder(self, request):
        """
        Expects payload:
        [
            {"id": 3, "order_index": 1},
            {"id": 1, "order_index": 2},
            {"id": 2, "order_index": 3}
        ]
        """
        try:
            data = request.data
            if not isinstance(data, list):
                return custom_api_response(
                    success=False, message="Invalid data format",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            serializer = HomeBannerReorderSerializer(data=data, many=True)

            if serializer.is_valid():
                for item in serializer.validated_data:
                    HomeBanner.objects.filter(id=item['id']).update(order_index=item['order_index'])
                return custom_api_response(success=True, message="Successfully updated!")

            return custom_api_response(
                success=False, message="Validation error",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            print('error reorder', e)
            url_routing_error(error=e)

