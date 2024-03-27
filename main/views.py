from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import UpdateProfileForm, UpdateUserForm
from .models import Profile, Tariff, SubscriptionPlan, Shop, UserProduct
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.http import JsonResponse
from django.db import models
from django.db.models import Sum



def home(request):
    return render(request, 'main/index.html')


def register(request):
    if request.method == "POST":
        username = request.POST.get('login')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        if pass1 != pass2:
            messages.info(request, "Пароли не совпадают")
            return redirect('/register')

        try:
            if User.objects.get(username=username):
                messages.warning(request, "Логин занят")
                return redirect('/register')

        except Exception as identifier:
            pass

        myuser = User.objects.create_user(username, email, pass1)
        myuser.save()
        messages.success(request, "Пользователь создан")
        return redirect('/login')

    return render(request, "main/register.html")


def handlelogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=username, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Вы успешно вошли")
            return redirect('/')
        else:
            messages.error(request, "Неправильные данные")
            return redirect('/login')

    return render(request, "main/login.html")


def handlelogout(request):
    logout(request)
    messages.success(request, "Вы успешно вышли")
    return redirect('/')


def profile(request):
    username = request.user
    posts = User.objects.filter(username=username)
    profile = Profile.objects.filter(user=username)
    context = {'posts': posts, 'profile': profile}
    return render(request, 'main/profile.html', context)



def update(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('/profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request, 'main/update.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def update_profile(request):
    if request.method == 'POST':
        selected_plan_id = request.POST.get('plan')

        # Получите объект выбранного плана подписки
        selected_plan = SubscriptionPlan.objects.get(pk=selected_plan_id)

        # Обновите профиль пользователя
        request.user.profile.selected_plan = selected_plan
        request.user.profile.save()

        # Другая логика обработки данных формы

    return redirect('profile')  # Замените 'profile' на имя вашего маршрута профиля

def tariff_view(request):
    if request.user.is_authenticated:
        tariffs = Tariff.objects.all()
        subscription_plans = SubscriptionPlan.objects.all()

        context = {
            'tariffs': tariffs,
            'subscription_plans': subscription_plans,
        }

        if request.method == 'POST':
            selected_tariff_name = request.POST.get('tariff', None)
            selected_plan_months = request.POST.get('plan', None)

            if selected_tariff_name and selected_plan_months:
                selected_tariff = Tariff.objects.get(name=selected_tariff_name)
                selected_plan = SubscriptionPlan.objects.get(months=selected_plan_months)

                # Создаем или обновляем профиль пользователя с информацией о выбранном тарифе
                profile, created = Profile.objects.get_or_create(user=request.user)
                profile.selected_tariff = selected_tariff
                profile.selected_plan = selected_plan
                profile.save()

                messages.success(request, f'Тариф "{selected_tariff_name}" выбран успешно!')
                return redirect('/profile')
            else:
                messages.error(request, 'Не удалось выбрать тариф. Пожалуйста, попробуйте еще раз.')

        return render(request, 'main/tariff.html', context)
    else:
        return redirect('/login')

def basket(request):
    if request.user.is_authenticated:
        # Получаем товары, добавленные текущим пользователем в корзину
        cart_items = UserProduct.objects.filter(user=request.user, is_purchased=False)

        # Вычисляем итоговую сумму
        total_price = cart_items.aggregate(total_price=Sum(models.F('product__price') * models.F('quantity')))['total_price']

        return render(request, 'main/basket.html', {'cart_items': cart_items, 'total_price': total_price})
    else:
        return redirect('/login')

# def shop(request):
#     return render(request, "main/shop.html")

@login_required
def stat(request):
    if request.user.is_superuser:
        return render(request, "main/stat.html")
    else:
        return render(request, 'main/index.html')
def catalog(request):
    # Получаем все объекты Shop из базы данных
    products = Shop.objects.all()


    # Передаем список товаров в контекст шаблона
    context = {'products': products}

    # Рендерим шаблон с контекстом
    return render(request, 'main/shop.html', context)


def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Shop, pk=product_id)
        user = request.user

        # Проверяем, есть ли уже такой товар в корзине пользователя
        user_product, created = UserProduct.objects.get_or_create(user=user, product=product)

        # Если товар уже был в корзине, увеличиваем количество
        if not created:
            user_product.quantity += 1
            user_product.save()

        return redirect('basket')
    else:
        return redirect('/login')

def remove_from_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Shop, id=product_id)

    # Найдем запись о товаре в корзине пользователя
    user_product = get_object_or_404(UserProduct, user=user, product=product)

    # Удаляем товар из корзины
    user_product.delete()

    return JsonResponse({'message': 'Товар удален из корзины'})
def update_quantity(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = get_object_or_404(Shop, id=product_id)

        # Найдем запись о товаре в корзине пользователя
        user_product = get_object_or_404(UserProduct, user=user, product=product)

        # Обновим количество товара в корзине
        new_quantity = int(request.POST.get('quantity', 1))
        user_product.quantity = new_quantity
        user_product.save()

        return JsonResponse({'message': 'Количество товара в корзине обновлено'})

    return JsonResponse({'message': 'Метод не разрешен'}, status=405)

def tariff_statistics(request):
    # Получаем данные о статистике тарифов
    tariff_data = get_tariff_statistics()

    # Возвращаем данные в формате JSON
    return JsonResponse(tariff_data)



def get_tariff_statistics():
    # Реализуйте логику для получения статистики тарифов
    # Например, можно использовать агрегации для подсчета количества каждого тарифа
    tariff_counts = Profile.objects.values('selected_tariff__name').annotate(count=models.Count('selected_tariff'))

    # Создаем списки меток и данных для диаграммы
    chart_labels = [count['selected_tariff__name'] for count in tariff_counts]
    chart_data = [count['count'] for count in tariff_counts]

    # Возвращаем данные
    return {'labels': chart_labels, 'data': chart_data}

def product_statistics(request):
    # Получаем данные о статистике тарифов
    product_data = get_product_statistics()

    # Возвращаем данные в формате JSON
    return JsonResponse(product_data)

def get_product_statistics():
    # Реализуйте логику для получения статистики по купленным товарам
    # Например, можно использовать агрегации для подсчета количества каждого купленного товара
    product_counts = UserProduct.objects.filter(is_purchased=True).values('product__name').annotate(count=models.Sum('quantity'))

    # Создаем списки меток и данных для диаграммы
    chart_labels = [count['product__name'] for count in product_counts]
    chart_data = [count['count'] for count in product_counts]

    # Возвращаем данные
    return {'labels': chart_labels, 'data': chart_data}

def checkout(request):
    if request.method == 'POST':
        # Обновляем поле is_purchased для всех товаров в корзине текущего пользователя
        UserProduct.objects.filter(user=request.user, is_purchased=False).update(is_purchased=True)

        return JsonResponse({'message': 'Заказ оформлен успешно'})

    return JsonResponse({'message': 'Метод не разрешен'}, status=405)