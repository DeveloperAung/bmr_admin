from django.urls import path
from . import views

urlpatterns = [
    path('list', views.membership_list, name='membership_list'),
]
