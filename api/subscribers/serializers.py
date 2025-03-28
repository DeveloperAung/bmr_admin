from rest_framework import serializers
from .models import SubscriberUser


class SubscriberUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriberUser
        fields = ['id', 'uuid', 'email', 'subscrd_flag', 'last_sent_at', 'created_at', 'created_by']


class SubscriberUserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriberUser
        fields = [
            'id', 'uuid', 'email', 'subscrd_flag', 'last_sent_at'
        ]


class SubscriberUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscriberUser
        fields = ['subscrd_flag']


class SubscriberUserBulkCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberUser
        fields = ['email']
