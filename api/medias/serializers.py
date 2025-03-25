from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from .models import Media, MediaJoins


class MediaListSerializer(serializers.ModelSerializer):
    event_titles = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = ['id', 'uuid', 'title', 'event_titles', 'created_at']

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_event_titles(self, obj):
        joins = obj.media_joins.all()
        unique_titles = set()
        for join in joins:
            if join.event and join.event.title:
                unique_titles.add(join.event.title)
        return list(unique_titles)


class MediaRetrieveSerializer(serializers.ModelSerializer):
    event_titles = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = [
            'id', 'uuid', 'title', 'event_titles', 'file_name', 'file_path', 'file_type', 'embed_code', 'location',
            'media_info',
            'created_at', 'created_by', 'modified_at', 'modified_by'
        ]

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_event_titles(self, obj):
        joins = obj.media_joins.all()
        unique_titles = set()
        for join in joins:
            if join.event and join.event.title:
                unique_titles.add(join.event.title)
        return list(unique_titles)


class MediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['title', 'media_info', 'location', 'file_path', 'embed_code', 'file_type']


class MediaJoinsListSerializer(serializers.ModelSerializer):
    media_title = serializers.CharField(source="media.title", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_sub_category_title = serializers.CharField(source="event.sub_category.title", read_only=True)

    class Meta:
        model = MediaJoins
        fields = ['id', 'uuid', 'media_title', 'event_title', 'event_sub_category_title']


class MediaJoinsRetrieveSerializer(serializers.ModelSerializer):
    media_title = serializers.CharField(source="media.title", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_sub_category_title = serializers.CharField(source="event.sub_category.title", read_only=True)

    class Meta:
        model = MediaJoins
        fields = [
            'id', 'uuid', 'media_title', 'event_title', 'event_sub_category_title',
                  'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class MediaJoinsCreateSerializer(serializers.ModelSerializer):
    # category = serializers.PrimaryKeyRelatedField(queryset=EventCategory.objects.all())

    class Meta:
        model = MediaJoins
        fields = ['media', 'event']


