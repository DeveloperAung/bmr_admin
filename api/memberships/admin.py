from django.contrib import admin
from .models import Membership, RegisteredUser


admin.site.register(Membership)
admin.site.register(RegisteredUser)

