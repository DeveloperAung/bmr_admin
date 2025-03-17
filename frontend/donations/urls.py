from django.urls import path
from . import views

urlpatterns = [
    path('', views.donation_list, name='donation_list'),
    path('create', views.donation_edit, name='donation_edit')
]
