from django.conf import settings
from django.db import models

from api.core.models import BaseModel


def event_image_path(instance, filename):
    return "event/image/cover/{}/{}".format(instance.id, filename)


class EventCategory(BaseModel):
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'Event Categories'

    def __str__(self):
        return self.title


class EventSubCategory(BaseModel):
    title = models.CharField(max_length=250)
    event_category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, related_name='event_sub_category', null=True)

    class Meta:
        verbose_name_plural = 'Event Sub Categories'

    def __str__(self):
        return f'{self.event_category.title} - {self.title}'


class Event(BaseModel):
    title = models.CharField(max_length=1500)
    short_description = models.CharField(max_length=1500, blank=True)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    location = models.CharField(blank=True, max_length=1500)
    feature_image = models.CharField(blank=True, max_length=1500)
    cover_image = models.ImageField(upload_to=event_image_path, blank=True)
    is_registered = models.BooleanField(default=False)
    is_short_course = models.BooleanField(default=False)
    max_seat = models.IntegerField(default=0, blank=True)
    is_publish = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_published_by",
        null=True,
        blank=True,
    )
    media_sent_at = models.DateTimeField(null=True, blank=True)
    media_sent_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_media_sent_by",
        null=True,
        blank=True,
    )
    media_sent_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title.encode("utf-8", "ignore").decode("utf-8")


class EventDate(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_dates", null=True)
    event_date = models.DateField()
    from_time = models.TimeField(blank=True)
    to_time = models.TimeField(blank=True)

    def __str__(self):
        return f"{self.event.title} on {self.event_date}"


