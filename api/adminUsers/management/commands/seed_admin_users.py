# your_app/management/commands/seed_admin_users.py

import random
import uuid
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.hashers import make_password

from api.adminUsers.models import AdminUser, AdminUserRole

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with AdminUser test data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding AdminUsers..."))

        AdminUser.objects.all().delete()  # Optional: clear before seeding
        roles = list(AdminUserRole.objects.all())

        for i in range(100):
            username = fake.user_name() + str(i)  # ensure uniqueness
            email = fake.email()
            name = fake.name()
            contact = fake.phone_number()
            secondary_contact = fake.phone_number() if random.choice([True, False]) else None
            role = random.choice(roles) if roles else None

            AdminUser.objects.create(
                username=username,
                email=email,
                name=name,
                contact=contact,
                secondary_contact=secondary_contact,
                admin_user_role=role,
                password=make_password("admin123"),  # default password
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 100 AdminUser records."))
