from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='admin_logout'),

    path('', views.admin_user_list, name='admin_user_list'),
    path('register/', views.admin_user_register, name='admin_user_register'),
    path('edit/id=?<uuid:uuid>', views.admin_user_edit, name='admin_user_edit'),
    path("delete/id=?<uuid:uuid>/", views.admin_user_soft_delete, name="admin_user_soft_delete"),

    path('reset_password/', views.reset_password, name='reset_password'),
    path('d_reset_password/', views.d_reset_password, name='d_reset_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]
