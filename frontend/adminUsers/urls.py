from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('', views.admin_user_list, name='admin_user_list'),
    path('register/', views.register_admin_user, name='register_admin_user'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('d_reset_password/', views.d_reset_password, name='d_reset_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]
