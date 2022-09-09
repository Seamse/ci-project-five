from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.all_products, name='products'),
    path('int:<product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('addreview/<int:product_id>/', views.add_review, name="add_review"),
    path('editreview/<int:product_id>/<int:review_id>', views.edit_review, name="edit_review"),
    path('deletereview/<int:product_id>/<int:review_id>', views.delete_review, name="delete_review"),
]
