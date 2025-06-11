import random
from datetime import timedelta, timezone

from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model  # To get your User model

from faker import Faker

# Assuming your Notice model is in 'my_app.models'
from api.notices.models import Notice

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Seeds the database with 50 fake Notice records.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding 50 Notice records...")

        # Get existing users to assign as published_by.
        # If no users exist, create one or handle this case.
        users = User.objects.all()
        if not users.exists():
            self.stdout.write(self.style.WARNING(
                "No users found. Please create at least one user before running this command, "
                "or modify the command to create a default user."
            ))
            return

        notices_to_create = []
        for _ in range(50):
            # Generate dates
            published_at = fake.date_time_between(start_date='-2y', end_date='now', tzinfo=timezone.utc)

            # 50/50 chance for blank description
            description = fake.text(max_nb_chars=500) if random.random() < 0.5 else None

            # Some notices won't have a from_date/to_date
            from_date = None
            to_date = None
            if random.random() < 0.7:  # 70% chance to have a date range
                from_date = published_at + timedelta(days=random.randint(1, 30))
                to_date = from_date + timedelta(days=random.randint(7, 90))

            # Determine if it's published, usually true if published_at is set
            is_published = True if published_at else False

            notice = Notice(
                title=fake.sentence(nb_words=random.randint(5, 10)),
                description=description,
                from_date=from_date,
                to_date=to_date,
                is_published=is_published,
                published_at=published_at,
                published_by=random.choice(users),  # Assign a random existing user
            )
            notices_to_create.append(notice)

        Notice.objects.bulk_create(notices_to_create)

        self.stdout.write(self.style.SUCCESS('Successfully seeded 50 Notice records.'))
