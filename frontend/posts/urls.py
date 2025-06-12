from django.urls import path
from . import views

urlpatterns = [
    path('category', views.post_category_list, name='post_category_list'),
    path('category/create', views.post_category_create, name='post_category_create'),
    path('category/edit/id=?<uuid:uuid>', views.post_category_edit, name='post_category_edit'),
    path("category/delete/id=?<uuid:uuid>/", views.post_category_soft_delete, name="post_category_soft_delete"),

    # path('post/<string:category_title>', views.post_category_list, name='post_category_list'),
    path('weekly-activities', views.weekly_activities_list, name='weekly_activities_list'),
    # path('weekly-activities/create', views.weekly_activities_create, name='weekly_activities_create'),
    # path('weekly-activities/edit/id=?<uuid:uuid>', views.weekly_activities_edit, name='weekly_activities_edit'),
    # path("weekly-activities/delete/id=?<uuid:uuid>/", views.weekly_activities_soft_delete, name="weekly_activities_soft_delete"),
]
