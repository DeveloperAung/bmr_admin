from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterUserViewSet, MembershipViewSet, CheckEmailSendOTP, ConfirmOTPAndRegister


router = DefaultRouter()
router.register(r'register-user', RegisterUserViewSet, basename='register_user')
router.register(r'membership', MembershipViewSet, basename='membership')

urlpatterns = [
    path("", include(router.urls)),

    path('register/send-otp/', CheckEmailSendOTP.as_view(), name='send_otp'),
    path('register/confirm/', ConfirmOTPAndRegister.as_view(), name='confirm_otp'),

]
