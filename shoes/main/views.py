import calendar
from .Observer import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from authorization.models import CustomUser, User_role
from .models import *
from django.contrib import messages
from django.db import transaction


def check_if_subscriber(user, product):
    return Subscription.objects.filter(user=user, product=product).exists()

def lists(request, model_name):
    # Словник моделей для динамічного доступу
    models = {
        'orders': Orders,
        'users': CustomUser,
        'collections': Collection
    }

    # Отримання моделі на основі `model_name`
    model = models.get(model_name.lower())

    if not model:  # Якщо такої моделі немає, перенаправляємо на головну
        messages.error(request, "Неправильна назва моделі.")
        return redirect('main_app:lists', model_name='collections')

    # Перевірка ролі користувача
    if model == CustomUser:  # Якщо модель — це користувачі
        if not request.user.is_authenticated:
            messages.error(request, "Ви не авторизовані.")
            return redirect('authorization_app:login')

        if request.user.user_role != User_role.ADMIN.value:  # Тільки адміністратор може переглядати користувачів
            messages.error(request, "У вас немає прав доступу до цієї сторінки.")
            return redirect('main_app:lists', model_name='collections')

        # Якщо все гаразд, отримуємо список користувачів
        object_list = CustomUser.objects.all()
        users_roles = [role.name for role in User_role]  # Отримуємо ролі користувачів
        template_name = f'{model_name}_list.html'
        # Рендеримо список користувачів
        return render(request, template_name, {
            "users": object_list,
            'users_roles': users_roles,
            'title': 'Users'
        })

    # Якщо модель — це замовлення
    if model == Orders:
        if request.user.user_role == User_role.ADMIN.value:
            object_list = model.objects.all()
        else:
            object_list = model.objects.filter(o_user=request.user)

        fields = model._meta.fields
        template_name = f"main/{model_name.lower()}_list.html"
        # Рендеримо список замовлень
        return render(request, template_name, {
            'model_name': model._meta.verbose_name_plural.title(),
            'fields': fields,
            'object_list': object_list,
            'model_name_lower': model_name.lower(),
            'title': model_name.title(),
        })
    if model == Collection:
        object_list = model.objects.all()

        template_name = f"main/{model_name.lower()}_list.html"
        return render(request, template_name, {
            'model_name': model._meta.verbose_name_plural.title(),
            'object_list': object_list,
            'model_name_lower': model_name.lower(),
        })

def products_list(request):
    # Отримуємо параметри фільтрації та пошуку з GET-запиту
    sh_gender = request.GET.get('sh_gender')  # Фільтр за статтю
    model = request.GET.get('sh_model')          # Фільтр за моделлю
    search_query = request.GET.get('search', '')  # Пошук за назвою

    # Базовий запит
    products = Shoes.objects.all()

    # Застосування фільтрації за статтю
    if sh_gender:
        products = products.filter(sh_gender=sh_gender)

    # Застосування фільтрації за моделлю
    if model:
        products = products.filter(sh_model=model)

    # Застосування пошуку за назвою товару
    if search_query:
        products = products.filter(sh_name__icontains=search_query)

    subscribed_ids = []
    is_subscribed = False
    if request.user.is_authenticated:
        subscribed_ids = Subscription.objects.filter(user=request.user).values_list('product_id', flat=True)

    # Передача контексту у шаблон
    context = {
        'title': 'Products',
        'product_list': products,  # Список відфільтрованих продуктів
        'selected_gender': sh_gender,  # Обране значення статі
        'selected_model': model,       # Обране значення моделі
        'search_query': search_query,  # Пошуковий запит
        'is_subscribed': list(subscribed_ids),
        # Список унікальних значень для полів фільтрації
        'genders': Shoes.objects.values_list('sh_gender', flat=True).distinct(),
        'models': Shoes.objects.values_list('sh_model', flat=True).distinct(),
    }

    return render(request, 'main/index1.html', context)

def subscribe_for_item(request, product_id, user_id):
    user = CustomUser.objects.get(pk=user_id)
    product = Shoes.objects.get(pk=product_id)

    subject = ObserverManager.get_instance().subject

    if request.method == 'POST':
        if user.is_authenticated and product.id_shoes and product.sh_count == 0:
            subject.attach(user, product)
            print(f"Subscribed {user.username} to {product.sh_name}")

    return redirect('main_app:products_list')

def unsubscribe_from_item(request, product_id, user_id):
    subject = ObserverManager.get_instance().subject
    user = CustomUser.objects.get(pk=user_id)
    product = Shoes.objects.get(pk=product_id)

    if request.method == 'POST':
        if user.is_authenticated and product.id_shoes and product.sh_count == 0:
            subject.detach(user, product)
            print(f"Unsubscribed {user.username} from {product.sh_name}")

    return redirect('main_app:products_list')

@transaction.atomic
@login_required(login_url='authorization_app:login')
def delete_view(request, model_name, pk):
    # Карта моделей для видалення
    model_map = {
        'shoes': Shoes,
        'orders': Orders,
        'users': CustomUser,
    }

    # Отримуємо модель за назвою
    model = model_map.get(model_name.lower())
    if not model:
        return render(request, 'main/index.html', {'message': 'Model not found'})

    # Отримуємо екземпляр об'єкта
    instance = get_object_or_404(model, pk=pk)

    # Перевірка прав доступу для адміністратора або власника
    if model_name.lower() == 'orders' and not (request.user.is_staff or request.user.is_superuser or request.user.user_role == User_role.ADMIN.value):
        messages.error(request, 'You do not have permission to delete this order.')
        return redirect(reverse('main_app:lists', kwargs={'model_name': 'orders'}))

    if model_name.lower() == 'users' and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this user.')
        return redirect(reverse('main_app:users_list', kwargs={'model_name': 'users'}))

    if request.method == 'POST':
        # Для замовлень перевірка, чи вони створені менше ніж рік тому
        if model_name.lower() == 'orders':
            one_year_ago = timezone.now() - timedelta(days=365)
            if instance.o_date_created > one_year_ago:
                messages.error(request, 'You cannot delete orders that are less than one year old.')
                return redirect(reverse('main_app:list', kwargs={'model_name': 'orders'}))

        # Для продуктів видаляємо зображення з файлової системи
        if model_name.lower() == 'shoes':
            for image in instance.images.all():
                if image.image:
                    try:
                        os.remove(image.image.path)
                    except FileNotFoundError:
                        pass
            instance.images.all().delete()

        if model_name.lower() == 'collections':
            for image in instance.images.all():
                if image.image:
                    try:
                        os.remove(image.image.path)
                    except FileNotFoundError:
                        pass
            instance.images.all().delete()

        # Видаляємо сам об'єкт
        instance.delete()

        # Повідомлення про успіх
        messages.success(request, f'{model_name.capitalize()} deleted successfully.')

        # Повертаємо користувача до списку відповідних елементів
        if model_name.lower() == 'shoes':
            return redirect(reverse('main_app:products_list'))
        elif model_name.lower() == 'orders':
            return redirect(reverse('main_app:lists', kwargs={'model_name': 'orders'}), {'messages': messages.error})
        elif model_name.lower() == 'users':
            return redirect(reverse('authorization:delete_profile'))

    # Якщо це не POST, то перенаправляємо на головну
    return redirect(reverse('main_app:main'))



def analytics(request):
    analytics = Orders.calculate_analytics()

    total_current = analytics['total_sum_current_month'] or 0
    total_previous = analytics['total_sum_previous_month'] or 0

    drop_percentage = 0
    if total_previous > 0:
        drop_percentage = ((total_previous - total_current) / total_previous) * 100

    context = {
        'total_sum': round(analytics['total_sum'] or 0, 2),
        'average_sum': round(analytics['average_sum'] or 0, 2),
        'max_sum': round(analytics['max_sum'] or 0, 2),
        'min_sum': round(analytics['min_sum'] or 0, 2),
        'total_sum_for_current_month': round(total_current, 2),
        'calculate_percentage_drop': round(drop_percentage, 0),
    }

    return render(request, 'main/index1.html', context)

def sales_chart(request):
        sales_data = Orders.get_sales_data()

        # Перетворення даних у формат, придатний для графіка
        labels = [calendar.month_name[month] for month in sales_data.keys()]
        data = lists(sales_data.values())

        return render(request, 'main/index.html', {
            'labels': labels,
            'data': data,
        })


@transaction.atomic
def create_order_with_items(order_data, items_data):
    order = Orders.objects.create(**order_data)
    for item in items_data:
        Orders.objects.create(order=order, **item)

@transaction.atomic
def update_stock(product_id, quantity):
    product = Shoes.objects.select_for_update().get(pk=product_id)
    if product.sh_count >= quantity:
        product.sh_count -= quantity
        product.save()
    else:
        raise ValueError("Not enough stock available")

@transaction.atomic
def test_atomicity():
    Orders.objects.create(o_sum=1000)
    raise ValueError("Simulated error")


