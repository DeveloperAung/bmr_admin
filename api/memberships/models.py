from django.db import models

from api.core.models import BaseModel


def profile_image_path(instance, filename):
    return "member/profile/{}/{}".format(instance.id, filename)


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
    registered_user = models.ForeignKey(
        RegisteredUser, on_delete=models.SET_NULL, related_name='membership_registered_user', null=True
    )
    nric_fin = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=3, choices=GENDER_CHOICES)
    dob = models.DateTimeField(blank=True, null=True)
    secondary_mobile = models.CharField(max_length=20, blank=True, null=True)
    city_of_birth = models.CharField(max_length=200, blank=True, null=True)
    country_of_birth = models.CharField(max_length=200, blank=True, null=True)
    residential_status = models.CharField(max_length=5, blank=True, null=True)
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
`
    def __str__(self):
        return self.title


