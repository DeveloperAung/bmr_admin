from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('create', views.notice_create, name='notice_create'),
    path('edit/id=?<uuid:uuid>', views.notice_edit, name='notice_edit'),
    path('delete/id=?<uuid:uuid>', views.notice_soft_delete, name='notice_delete'),
    path('publish-toggle/id=?<uuid:uuid>', views.notice_publish_toggle, name='notice_publish_toggle'),
]
