from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostCategoryViewSet, PostViewSet


router = DefaultRouter()
router.register(r'post', PostViewSet, basename='post')
router.register(r'category', PostCategoryViewSet, basename='post_category')

urlpatterns = [
    path("", include(router.urls)),
]
