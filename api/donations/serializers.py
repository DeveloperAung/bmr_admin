from rest_framework import serializers
from .models import DonationCategory, DonationSubCategory


class DonationCategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = DonationCategory
        fields = ['id', 'uuid', 'title', 'is_date_required', 'is_multi_select_required']


class DonationCategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCategory
        fields = [
            'id', 'uuid', 'title', 'is_date_required', 'is_multi_select_required',
                  'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class DonationCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DonationCategory
        fields = ['title', 'is_date_required', 'is_multi_select_required']


class DonationSubCategoryListSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="donation_category.title", read_only=True)

    class Meta:
        model = DonationSubCategory
        fields = ['id', 'uuid', 'title', 'category_title', 'donation_category']


class DonationSubCategoryRetrieveSerializer(serializers.ModelSerializer):
    category_title = serializers.CharField(source="donation_category.title", read_only=True)

    class Meta:
        model = DonationSubCategory
        fields = [
            'id', 'uuid', 'title', 'donation_category', 'category_title',
                  'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class DonationSubCategoryCreateSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=EventCategory.objects.all())

    class Meta:
        model = DonationSubCategory
        fields = ['title', 'donation_category']
