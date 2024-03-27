# Generated by Django 5.0 on 2023-12-18 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_tariff'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('months', models.IntegerField(verbose_name='Количество месяцев')),
                ('coefficient', models.FloatField(verbose_name='Коэффициент')),
            ],
            options={
                'verbose_name': 'План подписки',
                'verbose_name_plural': 'Планы подписок',
            },
        ),
    ]