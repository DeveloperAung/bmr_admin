from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeBannerViewSet


router = DefaultRouter()
router.register(r'home-banner', HomeBannerViewSet, basename='home_banner')

urlpatterns = [
    path("", include(router.urls)),
]
