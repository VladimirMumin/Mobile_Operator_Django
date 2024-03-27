# Generated by Django 5.0 on 2023-12-18 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_profile_selected_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='coach',
        ),
        migrations.RemoveField(
            model_name='card',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='card',
            name='gym',
        ),
        migrations.RemoveField(
            model_name='card',
            name='schedule',
        ),
        migrations.RemoveField(
            model_name='card',
            name='user',
        ),
        migrations.RemoveField(
            model_name='coach',
            name='gym',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='coach',
        ),
        migrations.RemoveField(
            model_name='gym',
            name='workouts',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='gym',
        ),
        migrations.DeleteModel(
            name='CardPlan',
        ),
        migrations.DeleteModel(
            name='Card',
        ),
        migrations.DeleteModel(
            name='Coach',
        ),
        migrations.DeleteModel(
            name='Workouts',
        ),
        migrations.DeleteModel(
            name='Gym',
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
    ]
