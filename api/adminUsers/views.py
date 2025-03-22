from drf_spectacular import openapi
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.adminUsers.serializers import LogoutSerializer
from api.utlis import custom_api_response


@extend_schema(
    tags=["Auth"],
    request=TokenObtainPairSerializer,
    responses={200: OpenApiResponse(description="Access and refresh tokens")},
)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return custom_api_response(success=True, message="Login successful", data=response.data)
        return custom_api_response(success=False, message="Invalid credentials", status_code=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Auth"],
    request=TokenRefreshSerializer,
    responses={200: OpenApiResponse(description="New access token")},
)
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return custom_api_response(success=True, message="Token refreshed successfully", data=response.data)
        return custom_api_response(success=False, message="Invalid refresh token", status_code=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Auth"],
    request=LogoutSerializer,
    responses={200: OpenApiResponse(description="Logout success")}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def logout_view(request):
    """Logout and blacklist refresh token"""
    try:
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return custom_api_response(success=False, message="Refresh token is required", status_code=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return custom_api_response(success=True, message="Logged out successfully")
    except Exception as e:
        return custom_api_response(success=False, message="Invalid token", status_code=status.HTTP_400_BAD_REQUEST)



