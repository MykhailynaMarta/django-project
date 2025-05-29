from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

app_name='authorization_app'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm, template_name='authorization/login-form.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
]