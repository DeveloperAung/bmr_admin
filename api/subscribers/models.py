from django.db import models

from api.core.models import BaseModel


class SubscriberUser(BaseModel):
    email = models.EmailField()
    subscrd_flag = models.CharField(max_length=10, blank=True, null=True, default="P")
    last_sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email


