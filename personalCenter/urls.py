from django.contrib import admin
from django.urls import path
from . import views

app_name = 'personalCenter'
urlpatterns = [
    path('<int:uid>', views.center, name='center'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('follow/<int:uid>', views.follow, name='follow'),
    path('unfollow/<int:uid>', views.unfollow, name='unfollow'),
]
