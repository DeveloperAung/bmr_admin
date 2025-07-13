from django.db.models import Q
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound, NotAuthenticated, PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.adminUsers.models import AdminUser, AdminUserRole
from api.adminUsers.serializers import LogoutSerializer
from api.utlis import custom_api_response, url_routing_error
from .serializers import (
    AdminUserListSerializer,
    AdminUserRetrieveSerializer,
    AdminUserCreateUpdateSerializer,

    AdminUserRoleListSerializer,
    AdminUserRoleCreateSerializer,
    AdminUserRoleRetrieveSerializer
)
import logging
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist

from ..custom_pagination import CustomPagination
from ..services import BaseSoftDeleteViewSet

logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Auth"],
    request=TokenObtainPairSerializer,
    responses={200: OpenApiResponse(description="Access and refresh tokens")},
)
class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            # Get username and password from request
            username = request.data.get('username')
            password = request.data.get('password')
            
            if not username or not password:
                return custom_api_response(
                    success=False, 
                    message="Username and password required", 
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user exists and is active
            try:
                user = AdminUser.objects.get(username=username)
                if not user.is_active:
                    return custom_api_response(
                        success=False, 
                        message="Account deactivated", 
                        status_code=status.HTTP_400_BAD_REQUEST
                    )
            except ObjectDoesNotExist:
                return custom_api_response(
                    success=False, 
                    message="Invalid credentials", 
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            # Call parent method to validate credentials
            response = super().post(request, *args, **kwargs)
            
            if response.status_code == 200:
                return custom_api_response(
                    success=True, 
                    message="Login successful", 
                    data=response.data
                )
            else:
                # Handle other error responses from parent
                return custom_api_response(
                    success=False, 
                    message="Invalid credentials", 
                    status_code=status.HTTP_400_BAD_REQUEST
                )
                
        except TokenError:
            return custom_api_response(
                success=False, 
                message="Invalid credentials", 
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return custom_api_response(
                success=False, 
                message="Internal server error", 
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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


@extend_schema(tags=["Admin Users"])
class AdminUserViewSet(viewsets.ModelViewSet):

    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        queryset = AdminUser.objects.filter(is_active=True).order_by('-date_joined')
        search = self.request.query_params.get("search")
        role = self.request.query_params.get("role")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(contact__icontains=search)
            )

        if role:
            queryset = queryset.filter(admin_user_role__id=role)

        return queryset

    def handle_authentication_error(self, request):
        """
        Returns an error response if authentication fails.
        """
        try:
            self.check_permissions(request)
            return None
        except NotAuthenticated:
            return custom_api_response(success=False, message="Authentication required",
                                       status_code=status.HTTP_401_UNAUTHORIZED)
        except PermissionDenied:
            return custom_api_response(success=False, message="Permission denied",
                                       status_code=status.HTTP_403_FORBIDDEN)

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return AdminUserListSerializer
            elif self.action == "retrieve":
                return AdminUserRetrieveSerializer
            elif self.action == "create":
                return AdminUserCreateUpdateSerializer
            elif self.action in ["update", "partial_update"]:
                return AdminUserCreateUpdateSerializer
            return AdminUserListSerializer
        except Exception as e:
            url_routing_error(error=e)

    def create(self, request, *args, **kwargs):
        auth_error = self.handle_authentication_error(request)
        if auth_error:
            return auth_error
        try:
            serializer = AdminUserCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return custom_api_response(
                    success=True, message="Created successfully", data=serializer.data,
                    status_code=status.HTTP_201_CREATED
                )

            return custom_api_response(
                success=False, message="Validation error", errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            print('create error', str(e))
            logger.error(f"Error creating object: {str(e)}")

            return custom_api_response(
                success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return custom_api_response(success=True, message="Data retrieved", data=serializer.data)
        except (NotFound, Http404):
            print('object not found')
            return custom_api_response(success=False, message="Record not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:

            error_title = type(e).__name__
            print('retrieve error', error_title)
            logger.error(f"Error retrieving object: {str(e)}")
            url_routing_error(error=error_title)
            # return custom_api_response(
            #     success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            # )

    def update(self, request, *args, **kwargs):
        auth_error = self.handle_authentication_error(request)
        if auth_error:
            return auth_error

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return custom_api_response(success=True, message="Updated successfully", data=serializer.data)
            return custom_api_response(
                success=False, message="Validation error", errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except (NotFound, Http404):
            return custom_api_response(success=False, message="Object not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('update error', str(e))
            logger.error(f"Error updating object: {str(e)}")
            return custom_api_response(
                success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        print('go inside delete')
        auth_error = self.handle_authentication_error(request)
        if auth_error:
            return auth_error

        try:
            instance = self.get_object()
            if not instance.is_active:
                return custom_api_response(
                    success=False, message="Record already deleted", status_code=status.HTTP_400_BAD_REQUEST
                )

            instance.is_active = False
            instance.deleted_at = now()
            instance.deleted_by = request.user
            instance.save()

            return custom_api_response(success=True, message="Record deleted successfully")
        except (NotFound, Http404):
            return custom_api_response(success=False, message="Object not found", status_code=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print('update error', str(e))
            logger.error(f"Error updating object: {str(e)}")
            return custom_api_response(
                success=False, message="Internal server error", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(tags=["Admin User Roles"])
class AdminUserRolesViewSet(BaseSoftDeleteViewSet):

    def get_serializer_class(self):
        try:
            if self.action == "list":
                return AdminUserRoleListSerializer
            elif self.action == "retrieve":
                return AdminUserRoleRetrieveSerializer
            elif self.action == "create":
                return AdminUserRoleCreateSerializer
            elif self.action in ["update", "partial_update"]:
                return AdminUserRoleCreateSerializer
            return AdminUserRoleListSerializer
        except Exception as e:
            url_routing_error(error=e)

    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return AdminUserRole.objects.filter(is_active=True).order_by('title')

