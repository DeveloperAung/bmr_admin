from django.db import models
from api.core.models import BaseModel
from django.conf import settings


def post_image_path(instance, filename):
    return "post/image/cover/{}/{}".format(instance.id, filename)


class PostCategory(BaseModel):
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'Post Categories'

    def __str__(self):
        return self.title


class Post(BaseModel):
    title = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_published_by",
        null=True,
        blank=True,
    )
    post_category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    # feature image
    cover_image = models.ImageField(upload_to=post_image_path, blank=True)
