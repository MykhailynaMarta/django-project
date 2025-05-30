from main.models import *
from django.shortcuts import render, get_object_or_404, redirect
from main.models import Shoes, Orders, ProductImage
from authorization.models import CustomUser, User_role
from add.forms import ProductCreateForm, OrderCreateForm, CollectionAddForm
from authorization.forms import CustomUserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
import json
from main.Observer import *

@login_required
def update_view(request, model_name, pk):
    # Карта моделей
    model = {
        'shoes': Shoes,
        'orders': Orders,
        'users': CustomUser,
        'collections': Collection,
    }.get(model_name.lower())

    if not model:
        return render(request, 'main/index.html', {'message': 'Model not found'})

    instance = get_object_or_404(model, pk=pk)

    # Перевірка прав доступу
    if model_name.lower() == 'orders' and not (request.user.is_staff or request.user.is_superuser or request.user.user_role == User_role.ADMIN.value):
        return render(request, 'main/index.html', {'message': 'Permission denied'})

    # Карта форм
    forms_map = {
        'shoes': ProductCreateForm,
        'orders': OrderCreateForm,
        'users': CustomUserCreationForm,
        'collections': CollectionAddForm,
    }
    form_class = forms_map.get(model_name.lower())

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()

            # Обробка нових зображень для продуктів
            if model_name.lower() == 'shoes' and 'new_images' in request.FILES:
                for image_file in request.FILES.getlist('new_images'):
                    ProductImage.objects.create(product=instance, image=image_file)

            if model_name.lower() == 'collections' and 'new_images' in request.FILES:
                for image_file in request.FILES.getlist('new_images'):
                    CollectionImage.objects.create(collection=instance, c_image=image_file)

            # Повернення до списку після збереження
            if model_name.lower() == 'shoes':
                return redirect('main_app:products_list')
            elif model_name.lower() == 'orders':
                return redirect('main_app:list', model_name='orders')  # Передаємо 'orders'
            elif model_name.lower() == 'users':
                return redirect('main_app:list', model_name='users')  # Передаємо 'users'
            elif model_name.lower() == 'collections':
                return redirect('main_app:lists', model_name='collections')

    else:
        form = form_class(request.POST or None, instance=instance)
    # Для продуктів отримуємо існуючі зображення
    existing_images = None
    if model_name.lower() == 'shoes':
        existing_images = instance.images.all()
    elif model_name.lower() == 'collections':
        existing_images = instance.c_images.all()

    template_name = (
            'add/product_add_form.html' if model_name.lower() == 'shoes'
            else 'add/order_create_form.html' if model_name.lower() == 'orders'
            else 'add/create_collection_modal.html' if model_name.lower() == 'collections'
            else 'main/index.html'
        )
    return render(request, template_name, {
        'form': form,
        'existing_images': existing_images,
        'action': 'Update',
        'is_editing': True,
        'title': f'Edit {model_name.capitalize()}',
    })

@login_required
def add_quantity(request, model_name, pk, user_id):

    # Карта моделей
    model = {
        'shoes': Shoes,
    }.get(model_name.lower())

    if not model:
        print(f'Model not found: {model_name}')
        return render(request, 'main/index.html', {'message': 'Model not found'})

    instance = get_object_or_404(model, pk=pk)

    # Перевірка прав доступу
    # if model_name.lower() == 'orders' and not (
    #         request.user.is_staff or request.user.is_superuser or request.user.user_role == User_role.ADMIN.value):
    #     print(f'Permission denied: {request.user}')
    #     return render(request, 'main/index.html', {'message': 'Permission denied'})

    user = CustomUser.objects.get(pk=user_id)
    # observer = ConcreteObserver(user)
    if request.method == 'POST':
        sh_count = int(request.POST.get('sh_count', 1))
        subject = ObserverManager.get_instance().subject
        instance.sh_count += sh_count

        subject._state = sh_count

        subject.notify(instance)
        print('Notify:')
        instance.save()

    return redirect('main_app:products_list')

@login_required
def minus_quantity(request, model_name, pk):

    # Карта моделей
    model = {
        'shoes': Shoes,
    }.get(model_name.lower())

    if not model:
        print(f'Model not found: {model_name}')
        return render(request, 'main/index.html', {'message': 'Model not found'})

    instance = get_object_or_404(model, pk=pk)

    # Перевірка прав доступу
    if model_name.lower() == 'orders' and not (
            request.user.is_staff or request.user.is_superuser or request.user.user_role == User_role.ADMIN.value):
        print(f'Permission denied: {request.user}')
        return render(request, 'main/index.html', {'message': 'Permission denied'})

    if request.method == 'POST':
        sh_count = int(request.POST.get('sh_count', 1))
        instance.sh_count -= sh_count
        instance.save()

    return redirect('main_app:products_list')


@csrf_exempt
def delete_image(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')
            image = get_object_or_404(ProductImage, id=image_id)
            image.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)


# Видалення запису
