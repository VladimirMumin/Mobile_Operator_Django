from django.contrib import admin
from django.shortcuts import render

from .models import Profile, Tariff, Shop, UserProduct


admin.site.register(Profile)
admin.site.register(Tariff)
admin.site.register(Shop)
admin.site.register(UserProduct)