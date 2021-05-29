from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('home', views.home),
    path('wish', views.wish),
    path('wish_detail/<int:wish_id>', views.wish_detail),
]