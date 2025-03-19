from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.adminUsers.urls')),
    path('contact-us/', include('api.contactUs.urls')),
    path('e/', include('api.events.urls')),
]
