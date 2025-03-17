import uuid

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now

from api.core.middleware import get_current_user


class AuditModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
    )
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_modified_by",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="%(class)s_deleted_by",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if isinstance(current_user, AnonymousUser):
            current_user = None

        if not self.pk:  # New instance
            if not self.created_by:  # Ensure it's only set once
                self.created_by = current_user

        self.modified_by = current_user  # Always update modified_by
        super().save(*args, **kwargs)
        # current_user = get_current_user()
        # if not self.pk:  # New instance
        #     self.created_by = current_user if current_user and current_user.is_authenticated else None
        # self.modified_by = current_user if current_user and current_user.is_authenticated else None
        # super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        current_user = get_current_user()
        if isinstance(current_user, AnonymousUser):
            current_user = None

        self.deleted_by = current_user
        self.deleted_at = now()
        self.is_active = False  # Mark as inactive instead of deleting
        self.save()

    class Meta:
        abstract = True


class BaseModel(AuditModelMixin):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)

    class Meta:
        abstract = True     # This makes it a base model and prevents table creation


