from django.urls import path
from . import views

urlpatterns = [
    path('home-setting-video-listing', views.home_setting_video_listing, name='home_setting_video_listing'),
    path('home-setting-video-edit', views.home_setting_video_edit, name='home_setting_video_edit'),

    path('home-banner-order', views.home_page_banner_order, name='home_page_banner_order'),
    path('home-banner-reorder', views.home_page_banner_reorder, name='home_page_banner_reorder'),
]
