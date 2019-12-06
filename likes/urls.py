from .views import *
from django.urls import path

# start with /likes/
urlpatterns = [
    path('collect_change', collect_change, name='collect_change'),
]
