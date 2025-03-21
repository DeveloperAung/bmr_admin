from django.contrib import admin
from .models import DonationCategory, DonationSubCategory, Donation


admin.site.register(Donation)
admin.site.register(DonationCategory)
admin.site.register(DonationSubCategory)

