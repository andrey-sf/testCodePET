# Generated by Django 5.0.4 on 2024-04-18 19:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Эл. почта')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Имя')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Админ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Зарегистрирован')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлен')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Подтвержден')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('occasion', models.CharField(choices=[('hiking', 'Поход'), ('wedding', 'Свадьба'), ('birthday', 'День рождения')], max_length=30, verbose_name='Повод')),
                ('description', models.TextField(verbose_name='Описание')),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма, которую запланировали собрать')),
                ('collected_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Собранная сумма')),
                ('contributors_count', models.PositiveIntegerField(default=0, verbose_name='Сколько человек уже сделало пожертвования')),
                ('cover_image', models.ImageField(blank=True, upload_to='collect_covers/', verbose_name='Обложка сбора')),
                ('end_datetime', models.DateTimeField(verbose_name='Дата и время завершения сбора')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Групповой сбор',
                'verbose_name_plural': 'Групповые сборы',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма пожертвования')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время пожертвования')),
                ('collect', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.collect', verbose_name='Сбор')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Платеж',
                'verbose_name_plural': 'Платежи',
            },
        ),
    ]
