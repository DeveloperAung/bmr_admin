from django.db import models
from api.core.models import BaseModel


class SinglePage(BaseModel):
    title = models.CharField(max_length=250)
    title_mm = models.CharField(max_length=250, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

