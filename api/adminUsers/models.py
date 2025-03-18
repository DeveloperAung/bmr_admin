from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid


class UserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,full_name=None, password=None):
        user = self.create_user(
                email,
                full_name=full_name,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, full_name=None, password=None):
        user = self.create_user(
                email,
                full_name=full_name,
                password=password,
                is_staff=True,
                is_admin=True
        )
        return user


class AdminUserRole(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class AdminUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    secondary_contact = models.CharField(max_length=150, blank=True, null=True)
    # admin_user_role = models.ForeignKey(AdminUserRole, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username


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

    def __str__(self):
        return self.user.username


class AdminUserRoleAuditLog(models.Model):
    """Tracks changes made to user records."""
    admin_user_role = models.ForeignKey(AdminUserRole, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=[("created", "Created"), ("updated", "Updated"), ("deleted", "Deleted")])
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="user_role_audit_performed_by"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
