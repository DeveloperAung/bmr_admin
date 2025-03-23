from rest_framework import serializers
from .models import PostCategory


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
        model = PostCategory
        fields = ['id', 'uuid', 'title']


class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'uuid', 'title', 'created_at', 'created_by', 'modified_at', 'modified_by']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['title']
