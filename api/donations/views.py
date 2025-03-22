import logging
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import DonationCategory, DonationSubCategory
from .serializers import (
    DonationCategoryListSerializer,
    DonationCategoryRetrieveSerializer,
    DonationCategoryCreateSerializer
)
from .serializers import (
    DonationSubCategoryListSerializer,
    DonationSubCategoryRetrieveSerializer,
    DonationSubCategoryCreateSerializer
)
from ..services import BaseSoftDeleteViewSet
from ..utlis import url_routing_error

logger = logging.getLogger(__name__)


@extend_schema(tags=["Donation Category"])
class DonationCategoryViewSet(BaseSoftDeleteViewSet):
    queryset = DonationCategory.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return DonationCategoryListSerializer
            elif self.action == "retrieve":
                return DonationCategoryRetrieveSerializer
            elif self.action == "create":
                return DonationCategoryCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return DonationCategoryCreateSerializer
            return DonationCategoryListSerializer
        except Exception as e:
            url_routing_error(error=e)


@extend_schema(tags=["Donation Sub Category"])
class DonationSubCategoryViewSet(BaseSoftDeleteViewSet):
    queryset = DonationSubCategory.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return DonationSubCategoryListSerializer
            elif self.action == "retrieve":
                return DonationSubCategoryRetrieveSerializer
            elif self.action == "create":
                return DonationSubCategoryCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return DonationSubCategoryCreateSerializer
            return DonationSubCategoryListSerializer
        except Exception as e:
            url_routing_error(error=e)
