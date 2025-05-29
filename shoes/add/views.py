from django.shortcuts import render, redirect
from pyexpat.errors import messages
from django.contrib import messages

from .forms import ProductCreateForm, OrderCreateForm, CollectionAddForm
from django.contrib.auth.decorators import login_required
from main.models import Shoes, ProductImage, Orders, Collection, CollectionImage


@login_required(login_url='authorization_app:login')
def collection_add(request):
    if request.method == 'POST':
        form = CollectionAddForm(request.POST)
        images = request.FILES.getlist('c_image')

        if form.is_valid():
            filter_kwargs = form.cleaned_data.copy()
            existing_collection = Collection.objects.filter(**filter_kwargs).first()

            if existing_collection:
                form.add_error(None, 'Така колекція вже існує.')
            else:
                collection = form.save()

                for image in images:
                    CollectionImage.objects.create(collection=collection, c_image=image)

                messages.success(request, "Колекцію успішно додано.")
                return redirect('main_app:lists', model_name='collections')
        else:
            print(form.errors)
    else:
        form = CollectionAddForm()

    return render(request, 'add/create_collection_modal.html', {
        'form': form,
        'action': 'add_app:collection_add',
        'title': 'Add Collection',
        'is_editing': False,
        'form_errors': form.errors,
    })
@login_required(login_url='authorization_app:login')
def product_add(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Отримуємо значення полів товару для перевірки
            name = form.cleaned_data['sh_name']
            model = form.cleaned_data['sh_model']
            size = form.cleaned_data['sh_size']
            color = form.cleaned_data['sh_color']
            manufacturer = form.cleaned_data['sh_manufacturer']
            gender = form.cleaned_data['sh_gender']

            # Перевірка на наявність товару з тими самими характеристиками
            existing_product = Shoes.objects.filter(
                sh_name=name,
                sh_model=model,
                sh_size=size,
                sh_color=color,
                sh_manufacturer=manufacturer,
                sh_gender=gender
            ).first()

            if existing_product:
                form.add_error(None, 'A product with these exact attributes already exists.')
            else:
                # Збереження продукту
                product = form.save(commit=False)
                product.save()

                # Додавання зображень
                images = request.FILES.getlist('sh_image')
                for image in images:
                    # Створення нового запису зображення для продукту
                    ProductImage.objects.create(product=product, image=image)

                print('Form is valid')
                return redirect('main_app:products_list')
        else:

            print(form.errors)
    else:
        form = ProductCreateForm()

    return render(request, 'add/product_add_form.html', {
        'form': form,
        'action': 'add_app:product_add',
        'title': 'Add Product',
        'is_editing': False,
        'messages': messages,
        'form_errors': form.errors,
    })



@login_required(login_url='authorization_app:login')
def orders_create(request, shoe_id=None):
    shoe = None
    if shoe_id:
        shoe = Shoes.objects.filter(pk=shoe_id).first()  # Отримуємо товар

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)  # Створюємо об'єкт, але не зберігаємо
            order.o_user = request.user  # Встановлюємо користувача
            if shoe:
                print(f"Shoe stock: {shoe.sh_count}, Ordered quantity: {order.o_count}")
            # Зменшення кількості товарів на складі
            if shoe and int(order.o_count) <= int(shoe.sh_count):  # Перевірка залишків
                shoe.sh_count -= int(order.o_count)  # Віднімаємо замовлену кількість
                shoe.save()  # Оновлюємо товар

                order.save()
                shoe.refresh_from_db()
                from main.Observer import ObserverManager
                subject = ObserverManager.get_instance().subject
                subject._state = shoe.sh_count
                print(f"Shoe stock after update: {shoe.sh_count}")
                return redirect('main_app:lists', model_name='orders')
            else:
                form.add_error('o_count', 'Not enough items in stock.')

    else:
        form_data = {'o_shoes': shoe} if shoe else {}
        form = OrderCreateForm(initial=form_data)

    return render(request, 'add/order_create_form.html', {
        'form': form,
        'user': request.user,
        'title': 'Create Order'
    })
