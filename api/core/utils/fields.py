import base64
import imghdr
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
    """
    A Django REST Framework field for handling image-uploads through raw post data.
    Expects a dict with keys: name, content (base64), content_type, size.
    """

    def to_internal_value(self, data):
        if isinstance(data, dict) and "content" in data:
            image_data = base64.b64decode(data["content"])
            image_name = data.get("name", str(uuid.uuid4()) + ".jpg")

            # Generate a ContentFile
            file = ContentFile(image_data, name=image_name)
            return super().to_internal_value(file)

        # fallback (for form uploads, etc.)
        return super().to_internal_value(data)
