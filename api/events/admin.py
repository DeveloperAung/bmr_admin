from django.contrib import admin
from .models import EventCategory, EventSubCategory, EventDate, Event


admin.site.register(EventCategory)
admin.site.register(EventSubCategory)
admin.site.register(Event)
admin.site.register(EventDate)
