from django.shortcuts import render
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import *
# Create your views here.

def home(request):
    return render(request, 'properties/home.html')

@cache_page(60 * 15) 
def property_list(request):
    properties = Property.objects.all()
    return JsonResponse({'data':list(properties.values())})