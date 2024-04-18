from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.models import Collect, Payment
from testCodePET import settings
from django.core.cache import cache


@receiver(post_save, sender=Collect)
def send_collect_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Создан новый сбор!'
        message = f'Был создан новый сбор "{instance.title}".'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = instance.author.email
        send_mail(subject, message, from_email, [recipient], fail_silently=False)


@receiver(post_save, sender=Payment)
def send_payment_creation_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Новый платеж!'
        message = f'Был сделан новый платеж на сумму {instance.amount} руб.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = instance.user.email
        send_mail(subject, message, from_email, [recipient], fail_silently=False)


@receiver([post_save, post_delete], sender=Collect)
@receiver([post_save, post_delete], sender=Payment)
def update_cache(sender, instance, **kwargs):
    # Очистить кэш при изменении или удалении объектов Collect или Payment
    cache.clear()
