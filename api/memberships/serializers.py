from rest_framework import serializers
from .models import RegisteredUser, Membership


class RegisteredUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisteredUser
        fields = ['id', 'uuid', 'name', 'email', 'mobile', 'created_at', 'created_by']


class RegisteredUserRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisteredUser
        fields = [
            'id', 'uuid', 'name', 'email', 'mobile',
                  'created_at', 'created_by', 'modified_at', 'modified_by'
        ]


class RegisteredUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RegisteredUser
        fields = ['name', 'email', 'mobile']


class MembershipListSerializer(serializers.ModelSerializer):
    registered_user = RegisteredUserListSerializer()

    class Meta:
        model = Membership
        fields = [
            'id', 'uuid', 'registered_user', 'membership_no',
            'membership_type', 'membership_status', 'registration_status', 'applied_date'
        ]


class MembershipRetrieveSerializer(serializers.ModelSerializer):
    registered_user = RegisteredUserRetrieveSerializer()
    secretary_admin_user = serializers.StringRelatedField()
    president_admin_user = serializers.StringRelatedField()
    cancelled_by = serializers.StringRelatedField()
    terminated_by = serializers.StringRelatedField()
    inactive_by = serializers.StringRelatedField()

    class Meta:
        model = Membership
        fields = '__all__'


class MembershipCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        exclude = ['uuid', 'created_at', 'created_by', 'modified_at', 'modified_by']
