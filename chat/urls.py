from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('room/<int:otherid>', views.room, name='room'),
    path('showhistory/', views.show_history, name='show_history'),
]
