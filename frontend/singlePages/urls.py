from django.urls import path
from . import views

urlpatterns = [
    path('single-page/list', views.single_page_list, name='single_page_list'),
    path('single-page/edit', views.single_page_edit, name='single_page_edit'),
]
