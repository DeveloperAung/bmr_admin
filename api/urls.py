from django.urls import path, include


urlpatterns = [
    path('auth/', include('api.adminUsers.urls')),
    path('contact-us/', include('api.contactUs.urls')),
    path('e/', include('api.events.urls')),
    path('d/', include('api.donations.urls')),
    path('p/', include('api.posts.urls')),
    path('h/', include('api.homePage.urls')),
    path('n/', include('api.notices.urls')),
]
