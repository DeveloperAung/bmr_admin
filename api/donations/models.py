from django.db import models

from api.core.models import BaseModel
from api.events.models import EventDate


class DonationCategory(BaseModel):
    title = models.CharField(max_length=250)
    is_date_required = models.BooleanField(default=True)
    is_multi_select_required = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Donation Categories'

    def __str__(self):
        return self.title


class DonationSubCategory(BaseModel):
    donation_category = models.ForeignKey(DonationCategory, on_delete=models.SET_NULL, blank=True, null=True,
                                          related_name='donation_sub_category')
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = 'Donation Sub Categories'

    def __str__(self):
        return self.title


class Donation(BaseModel):
    name = models.CharField(max_length=250)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    event = models.ForeignKey(EventDate, on_delete=models.SET_NULL, related_name='donation', blank=True, null=True)
    donation_sub_category = models.ForeignKey(DonationSubCategory, on_delete=models.SET_NULL, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
