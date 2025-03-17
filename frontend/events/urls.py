from django.urls import path
from . import views

urlpatterns = [
    # path('', views.dashboard, name='dashboard')

    path('', views.dhamma_class_list, name='dhamma_class_list'),
    path('create', views.dhamma_class_create, name='dhamma_class_create'),
]
