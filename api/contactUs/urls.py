# from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactUsViewSet

router = DefaultRouter()
router.register(r'', ContactUsViewSet, basename='contact-us')

urlpatterns = router.urls
