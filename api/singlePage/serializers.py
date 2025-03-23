from rest_framework import serializers
from .models import SinglePage


class SinglePageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SinglePage
        fields = ['id', 'uuid', 'title', 'title_mm', 'modified_at']


class SinglePageRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinglePage
        fields = [
            'id', 'uuid', 'title', 'title_mm', 'content', 'content_type',
            'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class SinglePageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SinglePage
        fields = ['title', 'title_mm', 'content', 'content_type']
