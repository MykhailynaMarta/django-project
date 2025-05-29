from django.urls import path
from . import views

app_name='add_app'

urlpatterns = [
    path('product/', views.product_add, name='product_add'),
    path('collection/', views.collection_add, name='collection_add'),
    path('order/<int:shoe_id>/', views.orders_create, name='orders_create'),
    # path('users/', views.users_list, name='users_list'),
]