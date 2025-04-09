from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import CustomTokenObtainPairView, logout_view, CustomTokenRefreshView, AdminUserViewSet, \
    AdminUserRolesViewSet

router = DefaultRouter()

router.register(r'admin-user', AdminUserViewSet, basename='admin-user')
router.register(r'admin-user-role', AdminUserRolesViewSet, basename='admin-user-role')

urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", logout_view, name="logout"),
]
