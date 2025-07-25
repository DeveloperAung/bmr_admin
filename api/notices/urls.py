from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NoticeViewSet


router = DefaultRouter()
router.register(r'notice', NoticeViewSet, basename='notice')

urlpatterns = [
    path("", include(router.urls)),
]
