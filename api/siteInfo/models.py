from django.db import models
from api.core.models import BaseModel


def site_file_path(instance, filename):
    return "site/media/file/{}/{}".format(instance.id, filename)


def social_media_file_path(instance, filename):
    return "site/social_media/file/{}/{}".format(instance.id, filename)


class SiteInfo(BaseModel):
    title = models.CharField(max_length=250)
    title_mm = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    description_mm = models.TextField(blank=True, null=True)
    favicon = models.FileField(upload_to=site_file_path, blank=True, null=True)
    logo = models.FileField(upload_to=site_file_path, blank=True, null=True)

    def __str__(self):
        return self.title


class SocialMedia(BaseModel):
    title = models.CharField(max_length=25)
    short_title = models.CharField(max_length=25)
    social_media_ico = models.FileField(upload_to=social_media_file_path, blank=True, null=True)
    social_media_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
