from django.db import models

from api.core.models import BaseModel
from api.events.models import Event


def media_file_path(instance, filename):
    return "media/file/{}/{}".format(instance.id, filename)


class Media(BaseModel):
    title = models.CharField(max_length=200)
    file_name = models.CharField(max_length=200, blank=True, null=True)
    file_path = models.FileField(upload_to=media_file_path, blank=True, null=True)
    file_type = models.CharField(max_length=200, blank=True, null=True)
    embed_code = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    media_info = models.DateTimeField(blank=True, null=True)
    downloaded_num = models.PositiveBigIntegerField()

    def __str__(self):
        return self.title


class MediaJoins(BaseModel):
    media = models.ForeignKey(Media, on_delete=models.SET_NULL, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True, related_name='event_media')

    class Meta:
        verbose_name_plural = 'Media Joins'

    def __str__(self):
        return f'{self.media.title} - {self.event.title}'
