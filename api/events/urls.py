from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventCategoryViewSet, EventSubCategoryViewSet


router = DefaultRouter()
router.register(r'event', EventViewSet, basename='event')
router.register(r'category', EventCategoryViewSet, basename='event_category')
router.register(r'sub-category', EventSubCategoryViewSet, basename='event-sub_category')

urlpatterns = [
    path("", include(router.urls)),
]
