from django.urls import path
from .views import *

urlpatterns = [
    path('', home , name='home'),
    path('property_list', property_list, name='property_list')
]
