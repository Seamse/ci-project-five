from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('make_purchase/', views.make_purchase, name='make_purchase'),
]
