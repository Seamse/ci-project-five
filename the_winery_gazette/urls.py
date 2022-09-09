from django.urls import path
from . import views


urlpatterns = [
    path('the_gazette/', views.the_gazette, name='the_gazette'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='gazette_post_detail'),
]
