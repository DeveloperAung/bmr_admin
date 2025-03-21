from django.conf import settings
from django.db import models

from api.core.models import BaseModel


def notice_image_path(instance, filename):
    return "notices/image/cover/{}/{}".format(instance.id, filename)


class Notice(BaseModel):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(blank=True, null=True)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_published_by",
        null=True,
        blank=True,
    )
    cover_image = models.FileField(upload_to=notice_image_path, blank=True, null=True)

    def __str__(self):
        return self.title


