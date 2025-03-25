import logging
from drf_spectacular.utils import extend_schema_view, extend_schema
from .models import Media, MediaJoins
from .serializers import (
    MediaListSerializer,
    MediaRetrieveSerializer,
    MediaCreateSerializer
)
from .serializers import (
    MediaJoinsListSerializer,
    MediaJoinsCreateSerializer,
    MediaJoinsRetrieveSerializer
)
from ..services import BaseSoftDeleteViewSet
from ..utlis import url_routing_error

logger = logging.getLogger(__name__)


@extend_schema(tags=["Media"])
class MediaViewSet(BaseSoftDeleteViewSet):
    queryset = Media.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return MediaListSerializer
            elif self.action == "retrieve":
                return MediaRetrieveSerializer
            elif self.action == "create":
                return MediaCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return MediaCreateSerializer
            return MediaListSerializer
        except Exception as e:
            # error_title = type(e).__name__
            # raise APIException(detail=f"Serializer selection failed: {error_title}")
            url_routing_error(error=e)


@extend_schema(tags=["Media Joins"])
class MediaJoinsViewSet(BaseSoftDeleteViewSet):
    queryset = MediaJoins.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return MediaJoinsListSerializer
            elif self.action == "retrieve":
                return MediaJoinsRetrieveSerializer
            elif self.action == "create":
                return MediaJoinsCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return MediaJoinsCreateSerializer
            return MediaJoinsListSerializer
        except Exception as e:
            # error_title = type(e).__name__
            # raise APIException(detail=f"Serializer selection failed: {error_title}")
            url_routing_error(error=e)
