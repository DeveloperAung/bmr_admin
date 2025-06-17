from rest_framework import serializers
from .models import PostCategory, Post
from ..core.utils.fields import Base64ImageField


class PostCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostCategory
        fields = ['id', 'uuid', 'title']


class PostCategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'uuid', 'title', 'created_at', 'created_by', 'modified_at', 'modified_by']


class PostCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['title']


class PostListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = [
            'id', 'uuid', 'title', 'is_published', 'published_at', 'published_by', 'post_category', 'parent',
            'short_description', 'description', 'modified_at'
        ]


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'uuid', 'title', 'short_description', 'description', 'is_published', 'created_at', 'created_by',
            'cover_image', 'post_category', 'modified_at', 'modified_by', 'published_at', 'published_by', 'parent'
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    cover_image = Base64ImageField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'short_description', 'description', 'is_published', 'post_category', 'cover_image']
