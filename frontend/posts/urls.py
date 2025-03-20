from django.urls import path
from . import views

urlpatterns = [
    path('category', views.post_category_list, name='post_category_list'),
    path('category/create', views.post_category_create, name='post_category_create'),
    path('category/edit/id=?<uuid:uuid>', views.post_category_edit, name='post_category_edit'),
    path("category/delete/id=?<uuid:uuid>/", views.post_category_soft_delete, name="post_category_soft_delete"),

]
