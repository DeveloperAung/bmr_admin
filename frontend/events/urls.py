from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name='dashboard')

    path('', views.dhamma_class_list, name='dhamma_class_list'),
    path('create', views.dhamma_class_create, name='dhamma_class_create'),
    path('details/id=?<uuid:event_uuid>', views.dhamma_class_details, name='dhamma_class_details'),

    path('category', views.event_category_list, name='event_category_list'),

    path('sub-category', views.event_sub_category_list, name='event_sub_category_list'),
]
