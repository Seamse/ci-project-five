from django.urls import path
from . import views

urlpatterns = [
    path('basket/', views.basket, name='basket'),
]
