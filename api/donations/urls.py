from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonationCategoryViewSet, DonationSubCategoryViewSet


router = DefaultRouter()

router.register(r'category', DonationCategoryViewSet, basename='donation_category')
router.register(r'sub-category', DonationSubCategoryViewSet, basename='donation_sub_category')

urlpatterns = [
    path("", include(router.urls)),
]
