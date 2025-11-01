from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import *
from .utils import get_all_properties
# Create your views here.

def home(request):
    return render(request, 'properties/home.html')

@cache_page(60 * 15) 
def property_list(request):
    properties = get_all_properties()
    return JsonResponse({'data':list(properties.values())})