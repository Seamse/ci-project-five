from django.urls import path
from . import views

urlpatterns = [
    path('', views.personal_account, name='account')
]
