import os
import django
import random
import uuid
from faker import Faker
from datetime import date

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CidProject.settings")
django.setup()

from core.models import AppUsageLog, Child, User, Municipality, AdministrativePost, Suco, Aldeia

fake = Faker()


def run():
    children = list(Child.objects.all())

    # 🔹 If no children exist, create 10 fake parents + children
    if not children:
        print("⚠️ No children found, creating 10 fake parents + children...")
        current_year = date.today().year

        for _ in range(10):
            # Pick random location hierarchy (already existing in DB)
            municipality = Municipality.objects.order_by("?").first()
            administrative_post = AdministrativePost.objects.filter(municipality=municipality).order_by("?").first() if municipality else None
            suco = Suco.objects.filter(administrative_post=administrative_post).order_by("?").first() if administrative_post else None
            aldeia = Aldeia.objects.filter(suco=suco).order_by("?").first() if suco else None

            # Create fake parent
            parent = User.objects.create_user(
                username=fake.user_name() + str(random.randint(1000, 9999)),
                whatsapp_number=f"+670{random.randint(70000000, 79999999)}",  # Timor-Leste range
                role="parent",
                email=fake.email(),
                password="test1234",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                address=fake.street_address(),
                municipality=municipality,
                administrative_post=administrative_post,
                suco=suco,
                aldeia=aldeia,
                is_verified=True,
            )

            # Decide year_of_birth and age_group
            year_of_birth = random.choice([current_year - 3, current_year - 4, current_year - 5, current_year - 6])
            age_group = "A" if year_of_birth in [current_year - 3, current_year - 4] else "B"

            # Create child for this parent
            child = Child.objects.create(
                parent=parent,
                first_name=fake.first_name(),
                year_of_birth=year_of_birth,
                age_group=age_group,
            )
            children.append(child)

    activity_choices = [c[0] for c in AppUsageLog.ACTIVITY_TYPE_CHOICES]
    age_group_choices = [c[0] for c in Child.AGE_GROUP_CHOICES]

    logs = []
    for _ in range(50):  # generate 50 logs
        child = random.choice(children)
        log = AppUsageLog(
            id=uuid.uuid4(),
            child=child,
            theme=fake.word().capitalize(),
            activity_type=random.choice(activity_choices),
            group=random.choice(age_group_choices),
            is_assessed=random.choice([True, False]),
            was_successful=random.choice([True, False]),
            date_accessed=fake.date_between(start_date="-30d", end_date="today"),
            duration_seconds=random.randint(30, 600),
        )
        logs.append(log)

    AppUsageLog.objects.bulk_create(logs)
    print(f"✅ Inserted {len(logs)} dummy AppUsageLog records.")
    print(f"👨‍👩‍👧‍👦 Parents created: {User.objects.filter(role='parent').count()}")
    print(f"🧒 Children created: {Child.objects.count()}")


if __name__ == "__main__":
    run()
