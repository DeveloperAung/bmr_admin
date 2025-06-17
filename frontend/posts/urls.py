from django.urls import path
from . import views

urlpatterns = [
    path('category', views.post_category_list, name='post_category_list'),
    path('category/create', views.post_category_create, name='post_category_create'),
    path('category/edit/id=?<uuid:uuid>', views.post_category_edit, name='post_category_edit'),
    path("category/delete/id=?<uuid:uuid>/", views.post_category_soft_delete, name="post_category_soft_delete"),

    # path('post/<string:category_title>', views.post_category_list, name='post_category_list'),
    path('weekly-activities', views.weekly_activities_list, name='weekly_activities_list'),
    path('weekly-activities/create', views.weekly_activity_create, name='weekly_activity_create'),
    path('weekly-activities/edit/id=?<uuid:uuid>', views.weekly_activity_edit, name='weekly_activity_edit'),

    path('article', views.article_list, name='article_list'),
    path('article/create', views.article_create, name='article_create'),
    path('article/edit/id=?<uuid:uuid>', views.article_edit, name='article_edit'),

    path("post/delete/id=?<uuid:uuid>/", views.post_soft_delete, name="post_soft_delete"),
    path('publish-toggle/id=?<uuid:uuid>', views.post_publish_toggle, name='post_publish_toggle'),
]
