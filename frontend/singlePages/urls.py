from django.urls import path
from . import views

urlpatterns = [
    path('', views.single_page_list, name='single_page_list'),
    path('create', views.single_page_create, name='single_page_create'),
    path('edit/id=?<uuid:uuid>', views.single_page_edit, name='single_page_edit'),
    path('delete/id=?<uuid:uuid>', views.single_page_soft_delete, name='single_page_delete'),
]
