from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta
from api.core.models import BaseModel


def profile_image_path(instance, filename):
    return "member/profile/{}/{}".format(instance.id, filename)


class CheckEmail(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)


class RegisteredUser(BaseModel):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Membership(BaseModel):
    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
    )
    RESIDENTIAL_STATUS = (
        ('sp', 's-pass'),
        ('ep', 'Employment Pass'),
        ('pr', 'Permanent Resident'),
        ('ctz', 'Citizen')
    )
    RESIDENTIAL_STATUS = (
        ('sp', 's-pass'),
        ('ep', 'Employment Pass'),
        ('pr', 'Permanent Resident'),
        ('ctz', 'Citizen')
    )
    MEMBERSHIP_TYPE = (
        ('associate', 'Associate'),
        ('others', 'Others'),
    )
    registered_user = models.ForeignKey(
        RegisteredUser, on_delete=models.SET_NULL, related_name='membership_registered_user', null=True
    )
    nric_fin = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    dob = models.DateTimeField(blank=True, null=True)
    secondary_mobile = models.CharField(max_length=20, blank=True, null=True)
    city_of_birth = models.CharField(max_length=200, blank=True, null=True)
    country_of_birth = models.CharField(max_length=200, blank=True, null=True)
    residential_status = models.CharField(max_length=5, choices=RESIDENTIAL_STATUS, blank=True, null=True)
    citizenship = models.CharField(max_length=200, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    occupation = models.CharField(max_length=200, blank=True, null=True)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.CharField(max_length=200, blank=True, null=True)
    company_contact_no = models.CharField(max_length=20, blank=True, null=True)
    profile_avatar = models.ImageField(blank=True, null=True, upload_to=profile_image_path)
    applied_date = models.DateTimeField(blank=True, null=True)
    educational_qualifications = models.CharField(max_length=200, blank=True, null=True)
    other_societies = models.CharField(max_length=200, blank=True, null=True)
    membership_type = models.CharField(max_length=200, choices=MEMBERSHIP_TYPE, blank=True, null=True)
    membership_no = models.CharField(max_length=20)
    secretary_admin_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="secretary_admin_user"
    )
    secretary_approved_date = models.DateTimeField(blank=True, null=True)
    president_admin_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="president_admin_user"
    )
    president_approved_date = models.DateTimeField(blank=True, null=True)
    registration_status = models.CharField(max_length=20)
    membership_status = models.BooleanField(default=False)
    cancelled_date = models.DateTimeField(blank=True, null=True)
    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cancelled_by"
    )
    terminated_date = models.DateTimeField(blank=True, null=True)
    terminated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="terminated_by"
    )
    inactive_date = models.DateTimeField(blank=True, null=True)
    inactive_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inactive_by"
    )

    def __str__(self):
        return self.registered_user.name





