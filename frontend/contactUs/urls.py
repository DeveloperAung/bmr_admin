from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_us_list, name='contact_us_list'),
    path('edit/id=?<uuid:uuid>/', views.contact_us_edit, name='contact_us_edit'),
    path("delete/id=?<uuid:uuid>/", views.soft_delete_contact, name="soft_delete_contact"),
]
