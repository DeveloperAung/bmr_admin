from django.contrib import admin
from .models import AdminUser, AdminUserRole


admin.site.register(AdminUser)
admin.site.register(AdminUserRole)
