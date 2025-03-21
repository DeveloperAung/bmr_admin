from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Schema View
schema_view = get_schema_view(
    openapi.Info(
        title="BMR API",
        default_version='v1',
        description="API documentation for the BMR Admin Panel",
        terms_of_service="https://bmr.sg/policies/terms/",
        contact=openapi.Contact(email="support@bmradmin.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],  # Adjust based on access control needs
    authentication_classes=[],
)
#
# security_definitions = [
#     openapi.SecurityRequirement({"Bearer": []}),
# ]
#
# schema_view.security = security_definitions

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),

    path('auth/', include('api.adminUsers.urls')),
    path('contact-us/', include('api.contactUs.urls')),
    path('e/', include('api.events.urls')),
    path('d/', include('api.donations.urls')),
    path('p/', include('api.posts.urls')),
    path('h/', include('api.homePage.urls')),
    path('n/', include('api.notices.urls')),
]
