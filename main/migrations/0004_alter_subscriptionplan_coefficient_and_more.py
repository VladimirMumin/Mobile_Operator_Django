# Generated by Django 5.0 on 2023-12-18 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_subscriptionplan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='coefficient',
            field=models.IntegerField(verbose_name='Коэффициент'),
        ),
        migrations.AlterField(
            model_name='subscriptionplan',
            name='months',
            field=models.CharField(max_length=30, verbose_name='Количество месяцев'),
        ),
    ]