from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, MembershipViewSet


router = DefaultRouter()
router.register(r'register-user', RegisterUserViewSet, basename='register_user')
router.register(r'membership', MembershipViewSet, basename='membership')

urlpatterns = [
    path("", include(router.urls)),
]
