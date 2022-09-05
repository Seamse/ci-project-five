from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.all_products, name='products'),
    path('<product_id>/', views.product_detail, name='product_detail'),
]
