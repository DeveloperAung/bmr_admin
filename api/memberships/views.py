import random

from rest_framework import status
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from api.services import BaseSoftDeleteViewSet
from .models import RegisteredUser, Membership, CheckEmail
from .serializers import (
    RegisteredUserListSerializer,
    RegisteredUserRetrieveSerializer,
    RegisteredUserCreateSerializer,

    MembershipListSerializer,
    MembershipRetrieveSerializer,
    MembershipCreateSerializer,

    RegistrationRequestSerializer, OTPVerificationSerializer,
)
import logging

from ..utlis import url_routing_error, custom_api_response

logger = logging.getLogger(__name__)


def generate_otp():
    return str(random.randint(100000, 999999))


@extend_schema(
    request=RegistrationRequestSerializer,
    tags=["Register User OTP Verification"])
class CheckEmailSendOTP(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            otp = generate_otp()
            pending, created = CheckEmail.objects.update_or_create(
                email=email,
                defaults={'otp': otp}
            )
            pending.save()

            # Send the OTP via email
            send_mail(
                'Your OTP Code',
                f'Use this code to verify your email: {otp}',
                'no-reply@example.com',
                [email]
            )

            return custom_api_response(success=True, message="OTP sent to email")
        return custom_api_response(success=False, message="Invalid data", errors=serializer.errors, status_code=400)


@extend_schema(
    # request=OTPVerificationSerializer,
    tags=["Register User OTP Verification"])
class ConfirmOTPAndRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            try:
                check_email = CheckEmail.objects.get(email=email, otp=otp, is_verified=False)
            except CheckEmail.DoesNotExist:
                return custom_api_response(success=False, message="Invalid OTP or email", status_code=400)

            if check_email.is_expired():
                return custom_api_response(success=False, message="OTP expired", status_code=400)

            # Create the actual user
            user = RegisteredUser.objects.create(
                username=email,
                email=email
            )

            check_email.is_verified = True
            check_email.save()

            return custom_api_response(success=True, message="Account created successfully")
        return custom_api_response(success=False, message="Invalid data", errors=serializer.errors, status_code=400)


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
