from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('make_purchase/', views.checkout, name='make_purchase'),
]
