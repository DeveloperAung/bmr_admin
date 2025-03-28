from rest_framework import serializers

from api.adminUsers.models import AdminUser


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class AdminUserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdminUser
        fields = ['id', 'uuid', 'name', 'username', 'email', 'contact']


class AdminUserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = [
            'id', 'uuid', 'name', 'username', 'email', 'contact', 'secondary_contact', 'date_joined'
        ]


class AdminUserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['name', 'username', 'email', 'contact', 'secondary_contact']

    def validate(self, attrs):
        errors = {}
        instance = self.instance  # Will be None on create, set on update

        # Username check
        username = attrs.get('username')
        if username:
            qs = AdminUser.objects.filter(username=username)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                errors['username'] = 'This username is already taken.'

        # Email check
        email = attrs.get('email')
        if email:
            qs = AdminUser.objects.filter(email=email)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                errors['email'] = 'This email is already in use.'

        # Contact check
        contact = attrs.get('contact')
        if contact:
            qs = AdminUser.objects.filter(contact=contact)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            if qs.exists():
                errors['contact'] = 'This contact number is already in use.'

        if errors:
            raise serializers.ValidationError(errors)

        return attrs

