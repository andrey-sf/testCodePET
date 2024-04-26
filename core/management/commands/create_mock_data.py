from django.core.management.base import BaseCommand
from core.models import Collect, Payment, Person
from core.resources import OCCASION
from faker import Faker
import random
from datetime import datetime, timedelta
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    help = 'Fill the database with mock data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        existing_emails = set(Person.objects.values_list('email', flat=True))
        new_persons = []
        while len(new_persons) < 2000:
            email = fake.email()
            if email not in existing_emails:
                existing_emails.add(email)
                new_persons.append(Person(email=email, password=fake.password(), name=fake.name()))
        Person.objects.bulk_create(new_persons)

        persons = list(Person.objects.all())

        occasion_list = [item[0] for item in OCCASION]

        collects = []
        payments = []
        for _ in range(20000):
            author = random.choice(persons)
            title = fake.sentence()
            occasion = random.choice(occasion_list)
            description = fake.paragraph()
            target_amount = round(random.uniform(100, 1000), 2)
            end_datetime = timezone.now() + timedelta(days=random.randint(1, 30))
            collects.append(Collect(
                author=author,
                title=title,
                occasion=occasion,
                description=description,
                target_amount=target_amount,
                end_datetime=end_datetime
            ))

        Collect.objects.bulk_create(collects)

        for collect in collects:
            for _ in range(random.randint(1, 10)):
                user = random.choice(persons)
                amount = round(random.uniform(10, 100), 2)
                timestamp = fake.date_time_between(start_date="-30d", end_date="now", tzinfo=None)
                payments.append(Payment(
                    user=user,
                    collect=collect,
                    amount=amount,
                    timestamp=timestamp
                ))

        with transaction.atomic():
            Payment.objects.bulk_create(payments)

            for collect in collects:
                payments_for_collect = Payment.objects.filter(collect=collect)
                collect.collected_amount = sum(payment.amount for payment in payments_for_collect)
                collect.contributors_count = payments_for_collect.count()
                collect.save()

        self.stdout.write(self.style.SUCCESS('Mock data created successfully'))
