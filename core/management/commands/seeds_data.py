# core/management/commands/seed_data.py

import random
import uuid
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import (
    Municipality, AdministrativePost, Suco, Aldeia,
    User, Child, AppUsageLog, PreschoolEnrollmentOptIn,
    ApkVersion, WhatsAppMessage
)

class Command(BaseCommand):
    help = "Seed the database with dummy data (100+ per table)"

    def handle(self, *args, **kwargs):
        fake = Faker()

        self.stdout.write(self.style.WARNING("Seeding database with dummy data..."))

        # -------------------------------
        # Municipalities
        # -------------------------------
        for i in range(100):
            Municipality.objects.get_or_create(name=fake.city())
        municipalities = list(Municipality.objects.all())

        # -------------------------------
        # Administrative Posts
        # -------------------------------
        for i in range(100):
            AdministrativePost.objects.get_or_create(
                municipality=random.choice(municipalities),
                name=fake.street_name()
            )
        admin_posts = list(AdministrativePost.objects.all())

        # -------------------------------
        # Suco
        # -------------------------------
        for i in range(100):
            Suco.objects.get_or_create(
                administrative_post=random.choice(admin_posts),
                name=fake.city_suffix()
            )
        sucos = list(Suco.objects.all())

        # -------------------------------
        # Aldeia
        # -------------------------------
        for i in range(100):
            Aldeia.objects.get_or_create(
                suco=random.choice(sucos),
                name=fake.word().capitalize()
            )
        aldeias = list(Aldeia.objects.all())

        # -------------------------------
        # Users
        # -------------------------------
        roles = ['parent', 'moe_admin', 'municipality_analyst', 'teacher']
        for i in range(100):
            try:
                User.objects.create_user(
                    username=f"user{i}",
                    whatsapp_number=fake.msisdn()[:15],
                    role=random.choice(roles),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    address=fake.address(),
                    municipality=random.choice(municipalities),
                    administrative_post=random.choice(admin_posts),
                    suco=random.choice(sucos),
                    aldeia=random.choice(aldeias),
                    password="password123"
                )
            except Exception:
                continue
        users = list(User.objects.all())

        # -------------------------------
        # Children
        # -------------------------------
        for i in range(100):
            Child.objects.create(
                parent=random.choice(users),
                first_name=fake.first_name(),
                year_of_birth=random.randint(2015, 2022),
                age_group=random.choice(['A', 'B'])
            )
        children = list(Child.objects.all())

        # -------------------------------
        # AppUsageLogs
        # -------------------------------
        activity_types = ['Numero', 'Lian', 'Arte', 'Motri', 'Sosyal']
        for i in range(100):
            AppUsageLog.objects.create(
                child=random.choice(children),
                theme=fake.word().capitalize(),
                activity_type=random.choice(activity_types),
                group=random.choice(['A', 'B']),
                is_assessed=random.choice([True, False]),
                was_successful=random.choice([True, False]),
                date_accessed=fake.date_between(start_date="-1y", end_date="today"),
                duration_seconds=random.randint(30, 600)
            )

        # -------------------------------
        # PreschoolEnrollmentOptIn
        # -------------------------------
        for u in users[:100]:
            PreschoolEnrollmentOptIn.objects.get_or_create(
                parent=u,
                contact_method=random.choice(['whatsapp', 'portal'])
            )

        # -------------------------------
        # APK Versions
        # -------------------------------
        for i in range(100):
            ApkVersion.objects.create(
                version_name=f"v{fake.random_int(1,10)}.{fake.random_int(0,9)}",
                download_url=fake.url(),
                is_latest=random.choice([True, False])
            )

        # -------------------------------
        # WhatsApp Messages
        # -------------------------------
        templates = ['verification', 'monthly_report', 'enrollment_info']
        statuses = ['sent', 'failed', 'delivered']
        for i in range(100):
            WhatsAppMessage.objects.create(
                to_number=fake.msisdn()[:15],
                template_type=random.choice(templates),
                content=fake.text(max_nb_chars=200),
                status=random.choice(statuses)
            )

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete (100+ records per table)."))
