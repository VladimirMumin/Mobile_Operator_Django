# Generated by Django 5.0 on 2023-12-18 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_shop_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='phones/', verbose_name='Ссылка на картинку'),
        ),
    ]