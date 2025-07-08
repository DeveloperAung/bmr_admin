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


class PermissionGroup(models.Model):
    """Group permissions by module/feature"""
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.display_name


class Permission(models.Model):
    """Individual permissions"""
    PERMISSION_TYPES = [
        ('create', 'Create'),
        ('view', 'View'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('soft_delete', 'Soft Delete'),
        ('publish', 'Publish'),
        ('unpublish', 'Unpublish'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('manage_users', 'Manage Users'),
        ('manage_roles', 'Manage Roles'),
        ('manage_permissions', 'Manage Permissions'),
        ('view_audit_logs', 'View Audit Logs'),
        ('custom', 'Custom'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    permission_type = models.CharField(max_length=20, choices=PERMISSION_TYPES)
    group = models.ForeignKey(PermissionGroup, on_delete=models.CASCADE, related_name='permissions')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['group__name', 'display_name']

    def __str__(self):
        return f"{self.group.display_name} - {self.display_name}"


class AdminUserRole(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def has_permission(self, permission_name):
        """Check if role has specific permission"""
        return self.permissions.filter(name=permission_name, is_active=True).exists()

    def has_permission_type(self, permission_type):
        """Check if role has permission type"""
        return self.permissions.filter(permission_type=permission_type, is_active=True).exists()

    def get_permissions_by_group(self):
        """Get permissions grouped by permission group"""
        permissions = {}
        for perm in self.permissions.filter(is_active=True).select_related('group'):
            if perm.group.name not in permissions:
                permissions[perm.group.name] = []
            permissions[perm.group.name].append(perm)
        return permissions


class AdminUser(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    secondary_contact = models.CharField(max_length=150, blank=True, null=True)
    admin_user_role = models.ForeignKey(AdminUserRole, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username

    def has_permission(self, permission_name):
        """Check if user has specific permission"""
        if not self.admin_user_role or not self.admin_user_role.is_active:
            return False
        return self.admin_user_role.has_permission(permission_name)

    def has_permission_type(self, permission_type):
        """Check if user has permission type"""
        if not self.admin_user_role or not self.admin_user_role.is_active:
            return False
        return self.admin_user_role.has_permission_type(permission_type)

    def has_any_permission(self, permission_names):
        """Check if user has any of the specified permissions"""
        if not self.admin_user_role or not self.admin_user_role.is_active:
            return False
        return self.admin_user_role.permissions.filter(
            name__in=permission_names, 
            is_active=True
        ).exists()

    def has_all_permissions(self, permission_names):
        """Check if user has all of the specified permissions"""
        if not self.admin_user_role or not self.admin_user_role.is_active:
            return False
        user_permissions = set(
            self.admin_user_role.permissions.filter(is_active=True).values_list('name', flat=True)
        )
        return all(perm in user_permissions for perm in permission_names)


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
        return self.admin_user_role.title


class PermissionAuditLog(models.Model):
    """Tracks changes made to permissions."""
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=[("created", "Created"), ("updated", "Updated"), ("deleted", "Deleted")])
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="permission_audit_performed_by"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True)  # Store additional details about the change

    def __str__(self):
        return f"{self.permission.name} - {self.action}"
