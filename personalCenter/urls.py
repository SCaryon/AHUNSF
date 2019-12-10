from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:uid>', views.center, name='center'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('follow/', views.follow, name='follow'),
    path('unfollow/', views.unfollow, name='unfollow'),
    path('idols/', views.show_idols, name='show_idols'),
]
