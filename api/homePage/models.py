from django.db import models

from api.core.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class HomeBanner(BaseModel):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='home_banner_category', null=True)
    order_index = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title


