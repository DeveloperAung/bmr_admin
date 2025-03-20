from rest_framework import serializers
from .models import HomeBanner


class HomeBannerListSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = HomeBanner
        fields = ['id', 'uuid', 'title', 'category_title', 'category', 'order_index']


class HomeBannerRetrieveSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        model = HomeBanner
        fields = [
            'id', 'uuid', 'title', 'category', 'category_title', 'order_index',
                  'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class HomeBannerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = HomeBanner
        fields = ['title', 'category', 'order_index']
