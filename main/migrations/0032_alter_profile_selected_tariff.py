# Generated by Django 5.0 on 2023-12-23 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0031_alter_profile_selected_tariff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='selected_tariff',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.tariff'),
        ),
    ]
