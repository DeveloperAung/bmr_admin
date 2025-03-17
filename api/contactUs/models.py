from django.conf import settings
from django.db import models

from api.core.models import BaseModel


class ContactUs(BaseModel):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=500)
    message = models.CharField(max_length=5000)
    reply_message = models.TextField(blank=True, null=True)
    replied_date = models.DateTimeField(blank=True, null=True)
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_replied_by",
        null=True,
        blank=True,
    )


