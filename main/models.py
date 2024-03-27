from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Tariff(models.Model):
    name = models.CharField('Название тарифа', max_length=30)
    price = models.IntegerField('Цена', default=0)
    internet_amount = models.IntegerField('Количество интернета', default=0)
    minutes_amount = models.IntegerField('Количество минут', default=0)
    additional_services = models.CharField('Дополнительные услуги', max_length=100, default="Нет")
    unlimited_minutes = models.CharField('Безлимитные звонки на номера Волна связи', max_length=10, default="Нет")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

class SubscriptionPlan(models.Model):
    months = models.CharField('Количество месяцев', max_length=30)
    coefficient = models.IntegerField('Коэффициент')

    def __str__(self):
        return f'{self.months} месяцев, Коэффициент: {self.coefficient}'

    class Meta:
        verbose_name = 'План подписки'
        verbose_name_plural = 'Планы подписок'



class Shop(models.Model):
    name = models.CharField('Название товара', max_length=100)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    memory = models.IntegerField('Количество памяти', default=0)
    image = models.ImageField('Ссылка на картинку', null=True, blank=True)
    description = models.TextField('Описание', null=True)
    color = models.CharField("Цвет", max_length=10, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар в магазине'
        verbose_name_plural = 'Товары в магазине'




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True)
    phone_number = models.IntegerField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    selected_tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, blank=True)
    selected_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Заполните поле name значением username пользователя
        self.name = self.user.username
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class UserProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Shop, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Количество товара в корзине пользователя
    is_purchased = models.BooleanField(default=False)  # Новое поле для обозначения, куплен ли товар


    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

    class Meta:
        verbose_name = 'Товар пользователя'
        verbose_name_plural = 'Товары пользователей'




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

