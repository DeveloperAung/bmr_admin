from django.urls import path, include


urlpatterns = [
    path('dashboard/', include('frontend.dashboard.urls')),
    path('admin-users/', include('frontend.adminUsers.urls')),
    path('single-pages/', include('frontend.singlePages.urls')),
    path('contact-us/', include('frontend.contactUs.urls')),
    path('donations/', include('frontend.donations.urls')),
    path('events/', include('frontend.events.urls')),
    path('posts/', include('frontend.posts.urls')),
    path('home-page/', include('frontend.homePage.urls')),
]
