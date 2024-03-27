from django.urls import path, include
from .views import home, stat, checkout, product_statistics, tariff_statistics, register, handlelogin, handlelogout, update_quantity, profile, update, add_to_cart, tariff_view, basket, update_profile, remove_from_cart, catalog

urlpatterns = [
    path('home', home, name='home'),
    path('', home, name='home'),
    path('register', register, name='register'),
    path('login', handlelogin, name='auth'),
    path('logout', handlelogout, name='exit'),
    path('profile', profile, name='profile'),
    path('update', update, name='update'),
    path('shop', catalog, name='shop'),
    path('stat', stat, name='stat'),
    path('tariff', tariff_view, name='tariff_view'),
    path('basket', basket, name='basket'),
    path('update_profile/', update_profile, name='update_profile'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('update_quantity/<int:product_id>/', update_quantity, name='update_quantity'),
    path('tariff_statistics/', tariff_statistics, name='tariff_statistics'),
    path('product_statistics/', product_statistics, name='product_statistics'),
    path('checkout/', checkout, name='checkout'),

]
