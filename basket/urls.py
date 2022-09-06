from django.urls import path
from . import views

urlpatterns = [
    path('basket/', views.basket, name='basket'),
    path('add/<item_id>/', views.add_to_basket, name='add_to_basket'),
    path('delete/<item_id>/', views.delete_item, name='delete_item'),
]
