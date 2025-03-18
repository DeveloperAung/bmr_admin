from rest_framework import serializers
from .models import ContactUs
from django.utils.timezone import now


class ContactUsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ["id", "uuid", "name", "email", "subject", "message", "reply_message", "replied_date", "replied_by", "created_at"]
        read_only_fields = ["reply_message", "replied_date", "replied_by", "created_at"]


class ContactUsAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = [
            "id", "uuid", "name", "email", "subject", "message", "reply_message", "replied_date", "replied_by",
            "created_at", "created_by", "modified_at", "modified_by", "deleted_at", "deleted_by", "is_active"
        ]
        read_only_fields = ["uuid", "name", "email", "subject", "message", "replied_date", "replied_by",
                            "deleted_at", "deleted_by", "is_active"]

    def update(self, instance, validated_data):
        """
        Custom update logic to set replied_date and replied_by automatically.
        """
        request = self.context.get("request")
        user = request.user if request else None

        instance.reply_message = validated_data.get("reply_message", instance.reply_message)
        instance.replied_date = now()
        instance.replied_by = user
        instance.save()
        return instance

    def delete(self, instance):
        """Custom delete logic to perform soft delete"""
        request = self.context.get("request")
        user = request.user if request else None

        instance.soft_delete(user)
        return instance
