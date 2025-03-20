from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_list, name='donation_list'),
    path('create', views.donation_edit, name='donation_edit'),

    path('category', views.donation_category_list, name='donation_category_list'),
    path('category/create', views.donation_category_create, name='donation_category_create'),
    path('category/edit/id=?<uuid:uuid>', views.donation_category_edit, name='donation_category_edit'),
    path("category/delete/id=?<uuid:uuid>/", views.donation_category_soft_delete, name="donation_category_soft_delete"),

    path('sub-category', views.donation_sub_category_list, name='donation_sub_category_list'),
    path('sub-category/create', views.donation_sub_category_create, name='donation_sub_category_create'),
    path('sub-category/edit/id=?<uuid:uuid>', views.donation_sub_category_edit, name='donation_sub_category_edit'),
    path("sub-category/delete/id=?<uuid:uuid>/", views.donation_sub_category_soft_delete,
         name="donation_sub_category_soft_delete"),
]
