from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name='dashboard')

    path('', views.dhamma_class_list, name='dhamma_class_list'),
    path('create', views.dhamma_class_create, name='dhamma_class_create'),
    path('details/id=?<uuid:event_uuid>', views.dhamma_class_details, name='dhamma_class_details'),

    path('category', views.event_category_list, name='event_category_list'),
    path('category/create', views.event_category_create, name='event_category_create'),
    path('category/edit/id=?<uuid:uuid>', views.event_category_edit, name='event_category_edit'),
    path("category/delete/id=?<uuid:uuid>/", views.event_category_soft_delete, name="event_category_soft_delete"),

    path('sub-category', views.event_sub_category_list, name='event_sub_category_list'),
    path('sub-category/create', views.event_sub_category_create, name='event_sub_category_create'),
    path('sub-category/edit/id=?<uuid:uuid>', views.event_sub_category_edit, name='event_sub_category_edit'),
    path("sub-category/delete/id=?<uuid:uuid>/", views.event_sub_category_soft_delete,
         name="event_sub_category_soft_delete"),
]
