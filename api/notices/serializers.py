from rest_framework import serializers
from . models import Notice


class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'uuid', 'title', 'description', 'is_published', 'published_at', 'published_by']


class NoticeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            'id', 'uuid', 'title', 'description', 'is_published', 'published_at', 'published_by', 'cover_image' 
                  'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title', 'description', 'is_published', 'published_at', 'published_by']

