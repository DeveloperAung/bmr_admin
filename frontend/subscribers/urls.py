from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriber_list, name='subscriber_list'),
    path('create', views.subscribers_bulk_create, name='subscribers_bulk_create'),

    # path('delete/id=?<uuid:uuid>', views.single_page_soft_delete, name='single_page_delete'),
]
