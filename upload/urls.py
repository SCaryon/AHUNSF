from django.urls import path
from . import views

# start with /upload
urlpatterns = [
    path('addproduct/', views.add_product, name='add_product'),
    path('addwish/', views.add_wish, name='add_wish'),
]
