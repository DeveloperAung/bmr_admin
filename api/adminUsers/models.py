from django.db import models
from django.contrib.auth.models import AbstractUser
from api.core.models import BaseModel
from django.conf import settings
import uuid


class AdminUserRole(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class AdminUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    secondary_contact = models.CharField(max_length=150)
    admin_user_role = models.ForeignKey(AdminUserRole, on_delete=models.SET_NULL, blank=True)


class UserAuditLog(models.Model):
    """Tracks changes made to user records."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=[("created", "Created"), ("updated", "Updated"), ("deleted", "Deleted")])
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="user_audit_performed_by"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
