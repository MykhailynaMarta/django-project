from django.urls import path
from . import views

app_name='edit_app'

urlpatterns = [
    # path('/product/<id_shoes:pk>', views.product_edit, name='product_edit'),
    # path('users/', views.users_list, name='users_list'),
    path('<str:model_name>/update/<int:pk>', views.update_view, name='update'),
    path('<str:model_name>/user/<int:user_id>/add_quantity/<int:pk>', views.add_quantity, name='add_quantity'),
    path('<str:model_name>/minus_quantity/<int:pk>', views.minus_quantity, name='minus_quantity'),
    path('product/delete-image/', views.delete_image, name='delete_image'),
]