from django.db import models
from api.core.models import BaseModel


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
    post_category = models.ForeignKey(PostCategory, on_delete=models.SET_NULL, null=True)
    # feature image id
    # parent
    cover_image = models.ImageField(upload_to=post_image_path, blank=True)
