from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MediaViewSet, MediaJoinsViewSet


router = DefaultRouter()
router.register(r'media', MediaViewSet, basename='media')
router.register(r'media-joins', MediaJoinsViewSet, basename='media-joins')

urlpatterns = [
    path("", include(router.urls)),
]
