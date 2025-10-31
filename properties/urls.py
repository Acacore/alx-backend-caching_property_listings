from django.urls import path
from .views import *

urlpatterns = [
    path('', home , name='home'),
    path('properties_list', properties_list, name='properties_list')
]
