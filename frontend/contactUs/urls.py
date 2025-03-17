from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_us_list, name='contact_us_list'),
    path('edit', views.contact_us_edit, name='contact_us_edit'),
]
