# Generated by Django 5.0 on 2023-12-18 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_tariff_additional_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='unlimited_minutes',
            field=models.CharField(default='Нет', max_length=10, verbose_name='Безлимитные звонки на номера Волна связи'),
        ),
    ]
