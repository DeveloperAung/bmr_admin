from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema

from api.services import BaseSoftDeleteViewSet
from .models import RegisteredUser, Membership
from .serializers import (
    RegisteredUserListSerializer,
    RegisteredUserRetrieveSerializer,
    RegisteredUserCreateSerializer,

    MembershipListSerializer,
    MembershipRetrieveSerializer,
    MembershipCreateSerializer,
)
import logging
from ..utlis import url_routing_error, custom_api_response

logger = logging.getLogger(__name__)


@extend_schema(tags=["Register User"])
class RegisterUserViewSet(BaseSoftDeleteViewSet):
    queryset = RegisteredUser.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return RegisteredUserListSerializer
            elif self.action == "retrieve":
                return RegisteredUserRetrieveSerializer
            elif self.action == "create":
                return RegisteredUserCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return RegisteredUserCreateSerializer
            return RegisteredUserListSerializer
        except Exception as e:
            url_routing_error(error=e)


@extend_schema(tags=["Membership"])
class MembershipViewSet(BaseSoftDeleteViewSet):
    queryset = RegisteredUser.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return MembershipListSerializer
            elif self.action == "retrieve":
                return MembershipRetrieveSerializer
            elif self.action == "create":
                return MembershipCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return MembershipCreateSerializer
            return MembershipListSerializer
        except Exception as e:
            url_routing_error(error=e)
