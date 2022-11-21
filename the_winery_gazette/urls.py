from django.urls import path
from . import views


urlpatterns = [
    path('the_gazette/', views.the_gazette, name='the_gazette'),
    path('add_post/', views.add_post, name='add_post'),
    path('edit/<slug:slug>/', views.edit_post, name='edit_post'),
    path('delete/<slug:slug>/', views.delete_post, name='delete_post'),
    path('<slug:slug>/', views.post_detail, name='gazette_post_detail'),
]
