from rest_framework import serializers
from . models import Notice


class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            'id', 'uuid', 'title', 'description', 'from_date', 'to_date',
                  'is_published', 'published_at', 'published_by'
        ]


class NoticeRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            'id', 'uuid', 'title', 'description', 'from_date', 'to_date',
            'is_published', 'published_at', 'published_by', 'cover_image',
            'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class NoticeCreateSerializer(serializers.ModelSerializer):
    from_date = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d'])
    to_date = serializers.DateField(required=False, allow_null=True, input_formats=['%Y-%m-%d'])
    
    class Meta:
        model = Notice
        fields = ['title', 'description', 'from_date', 'to_date', 'is_published', 'published_at', 'published_by']

