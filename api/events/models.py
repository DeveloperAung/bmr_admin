from django.conf import settings
from django.db import models

from api.core.models import BaseModel


def event_image_path(instance, filename):
    return "event/image/cover/{}/{}".format(instance.title, filename)


class EventCategory(BaseModel):
    title = models.CharField(max_length=250)

    def __unicode__(self):
        return self.title


class EventSubCategory(BaseModel):
    title = models.CharField(max_length=250)
    event_category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, related_name='event_sub_category')

    def __unicode__(self):
        return f'{self.event_category.title} - {self.title}'


class Event(BaseModel):
    title = models.CharField(max_length=1500)
    short_description = models.CharField(max_length=1500, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(blank=True)
    feature_image = models.CharField(blank=True)
    cover_image = models.ImageField(upload_to=event_image_path, blank=True)
    is_registered = models.BooleanField(default=False)
    is_short_course = models.BooleanField(default=False)
    max_seat = models.IntegerField(default=0, blank=True)
    is_publish = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_published_by",
        null=True,
        blank=True,
    )
    media_sent_at = models.DateTimeField()
    media_sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_media_sent_by",
        null=True,
        blank=True,
    )
    media_sent_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_dates")
    event_date = models.DateField()
    from_time = models.TimeField(blank=True)
    to_time = models.TimeField(blank=True)

    def __str__(self):
        return f"{self.event.name} on {self.event_date}"


