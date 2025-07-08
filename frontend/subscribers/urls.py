from django.urls import path
from . import views

app_name = 'subscribers'

urlpatterns = [
    path('', views.subscriber_list, name='list'),
    path('create', views.subscribers_bulk_create, name='bulk_create'),
    path('edit/<uuid:uuid>', views.subscriber_edit, name='edit'),
    path('delete/<uuid:uuid>', views.subscriber_soft_delete, name='delete'),
]
