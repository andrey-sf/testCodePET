from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User
from django.db import models

from core.resources import OCCASION


class Collect(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Название')
    occasion= models.CharField(max_length=30, choices=OCCASION, verbose_name="Повод")
    description = models.TextField(verbose_name='Описание')
    target_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                        verbose_name='Сумма, которую запланировали собрать')
    collected_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Собранная сумма')
    contributors_count = models.PositiveIntegerField(default=0,
                                                     verbose_name='Сколько человек уже сделало пожертвования')
    cover_image = models.ImageField(upload_to='collect_covers/', verbose_name='Обложка сбора', blank=True)
    end_datetime = models.DateTimeField(verbose_name='Дата и время завершения сбора')

    class Meta:
        verbose_name = 'Групповой сбор'
        verbose_name_plural = 'Групповые сборы'

    def __str__(self) -> str:
        return str(self.title)

    def payments(self):
        return Payment.objects.filter(collect=self)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    collect = models.ForeignKey(Collect, on_delete=models.CASCADE, verbose_name='Сбор')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма пожертвования')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время пожертвования')

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self) -> str:
        return str(self.id)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            self.collect.collected_amount += self.amount
            self.collect.contributors_count += 1
            self.collect.save()

    def delete(self, *args, **kwargs):
        self.collect.collected_amount -= self.amount
        self.collect.contributors_count -= 1
        self.collect.save()
        super().delete(*args, **kwargs)


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=""):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=""):
        """
        Creates and saves a Superuser with the given email and password.
        """
        user = self.create_user(email=email, password=password, name=name)
        user.is_admin = True
        user.save(using=self._db)
        return user


# Custom User Model.
class Person(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Эл. почта",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255, blank=True, verbose_name="Имя")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_admin = models.BooleanField(default=False, verbose_name="Админ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Зарегистрирован")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    is_verified = models.BooleanField(("Подтвержден"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin