from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_app:lists', model_name='collections')
        else:
            print(form.errors)
            return render(request, 'authorization/authorization_form.html', {'form': form, 'form_method': 'authorization_app:register', 'title': 'Register'})
    else:
        form = CustomUserCreationForm()
        print(form.errors)
        return render(request, 'authorization/authorization_form.html', {'form': form, 'form_method': 'authorization_app:register', 'title': 'Register'})


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успіх!')
            return render(request, 'main/collections_list.html', {'form': form, 'form_method': 'authorization_app:edit_profile', 'title': 'Edit Profile'})
        else:
            print(form.errors)
            erors = form.errors
            return render(request, 'authorization/edit_profile.html', {'form': form, 'erors': erors, 'form_method': 'authorization_app:edit_profile', 'title': 'Edit Profile'})
    else:
        form = CustomUserChangeForm(instance=user)

    return render(request, 'authorization/edit_profile.html', {'form': form, 'form_method': 'authorization_app:edit_profile', 'title': 'Edit Profile'})


@login_required
def delete_profile(request):
    user = request.user
    if request.method == 'POST':
        user.delete()
        return redirect('main_app:lists', model_name='collections')
    return render(request, 'authorization/delete_profile.html', {'title': 'Delete Profile', 'form_method': 'authorization_app:delete_profile'})