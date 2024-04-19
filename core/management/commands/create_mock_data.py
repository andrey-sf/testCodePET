from django.core.management.base import BaseCommand
from core.models import Collect, Payment, Person
from core.resources import OCCASION
from faker import Faker
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Fill the database with mock data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        persons = []

        # Создание пользователей Person
        for _ in range(100):
            while True:
                email = fake.email()
                if not Person.objects.filter(email=email).exists():
                    break
            password = fake.password()
            name = fake.name()
            person = Person.objects.create_user(email=email, password=password, name=name)
            persons.append(person)

        occasion_list = [item[0] for item in OCCASION]

        # Создание коллекций и платежей
        for _ in range(2000):
            author = random.choice(persons)
            title = fake.sentence()
            occasion = random.choice(occasion_list)
            description = fake.paragraph()
            target_amount = round(random.uniform(100, 1000), 2)
            end_datetime = datetime.now() + timedelta(days=random.randint(1, 30))
            collect = Collect.objects.create(author=author, title=title, occasion=occasion, description=description,
                                             target_amount=target_amount, end_datetime=end_datetime)

            for _ in range(random.randint(1, 10)):
                user = random.choice(persons)
                amount = round(random.uniform(10, 100), 2)
                timestamp = fake.date_time_between(start_date="-30d", end_date="now", tzinfo=None)
                Payment.objects.create(user=user, collect=collect, amount=amount, timestamp=timestamp)

        self.stdout.write(self.style.SUCCESS('Mock data created successfully'))
