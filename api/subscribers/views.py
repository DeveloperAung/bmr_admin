from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema_view, extend_schema
from api.services import BaseSoftDeleteViewSet
from .models import SubscriberUser
from .serializers import (
    SubscriberUserCreateSerializer,
    SubscriberUserListSerializer,
    SubscriberUserRetrieveSerializer
)
from django.utils import timezone
import logging

from ..utlis import custom_api_response

logger = logging.getLogger(__name__)


@extend_schema(tags=["Single Page"])
class SubscriberViewSet(BaseSoftDeleteViewSet):
    queryset = SubscriberUser.objects.all().order_by('id')

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return SubscriberUserListSerializer
            elif self.action == "retrieve":
                return SubscriberUserRetrieveSerializer
            elif self.action == "create":
                return SubscriberUserCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return SubscriberUserCreateSerializer
            return SubscriberUserListSerializer
        except Exception as e:
            print('error', e)
            logger.error(f"Error selecting serializer: {e}")
            return Response({"error": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        queryset = SubscriberUser.objects.filter(is_active=True).order_by('-created_at')
        search = self.request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(uuid__icontains=search)
            )
        return queryset

    @action(detail=False, methods=['post'], url_path='bulk-create')
    def bulk_create(self, request):
        emails = request.data.get('emails', [])

        if not isinstance(emails, list):
            return Response({'detail': 'emails must be a list.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate all entries are strings and look like emails
        invalid_emails = [email for email in emails if not isinstance(email, str) or '@' not in email]
        if invalid_emails:
            return custom_api_response(
                success=False,
                message='Invalid email format or missing email.',
                errors={'invalid_entries': invalid_emails},
                status_code=status.HTTP_400_BAD_REQUEST
            )

        duplicates_in_request = [email for email in set(emails) if emails.count(email) > 1]

        existing_emails = list(
            SubscriberUser.objects.filter(email__in=emails).values_list('email', flat=True)
        )

        if duplicates_in_request or existing_emails:
            return custom_api_response(
                success=False,
                message='Duplicate or existing emails found.',
                errors={
                    'duplicates_in_request': duplicates_in_request,
                    'already_exists': existing_emails
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        subscribers = [SubscriberUser(email=email) for email in emails]
        SubscriberUser.objects.bulk_create(subscribers)

        return custom_api_response(
            success=True,
            message='Subscribers created successfully.',
            data={'created': [s.email for s in subscribers]},
            status_code=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["patch"], url_path="publish-toggle")
    def status_toggle(self, request, uuid=None):
        try:
            subscriber_user = self.get_object()
            try:
                is_active = "Y" if subscriber_user.subscrd_flag in ["P", "N"] else "N"
                subscriber_user.subscrd_flag = is_active

                subscriber_user.save()
                return custom_api_response(
                    success=True,
                    message=f"Update status successfully",
                    data={
                        "id": subscriber_user.id,
                        "subscrd_flag": subscriber_user.subscrd_flag
                    }
                )
            except subscriber_user.DoesNotExist:
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



