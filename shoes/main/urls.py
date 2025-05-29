from django.urls import path
from . import views

app_name='main_app'

urlpatterns = [
    path('/analytics', views.analytics, name='analytics'),
    # path('', views.index, name='index'),
    path('products/list/', views.products_list, name='products_list'),
    path('<str:model_name>/lists/', views.lists, name='lists'),
    path('delete/<str:model_name>/<int:pk>/', views.delete_view, name='delete'),
    path('subscribe/user/<int:user_id>/product/<int:product_id>', views.subscribe_for_item, name='subscribe_for_item'),
    path('unsubscribe/user/<int:user_id>/product/<int:product_id>', views.unsubscribe_from_item, name='unsubscribe_from_item'),
]