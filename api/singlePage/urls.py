from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SinglePageViewSet


router = DefaultRouter()
router.register(r'single-page', SinglePageViewSet, basename='single_page')

urlpatterns = [
    path("", include(router.urls)),
]
