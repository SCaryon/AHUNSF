from .views import *
from django.urls import path


# start with /square/
urlpatterns = [
    path('products', products_list, name='products'),
    path('products/type/<int:type_id>', products_list_with_type, name='products_list_with_type'),
    path('product/<int:product_id>', product_detail, name='product_detail'),

    path('wishes', wishes_list, name='wishes'),
    path('wishes/type/<int:type_id>', wishes_list_with_type , name='wishes_list_with_type'),
    path('wish/<int:wish_id>', wish_detail, name='wish_detail'),
]
