from django.urls import path
from . import views


urlpatterns = [
    path('the_gazette/', views.the_gazette, name='the_gazette'),
    path('add_post/', views.add_post, name='add_post'),
    path('<slug:slug>/', views.post_detail, name='gazette_post_detail'),
]
