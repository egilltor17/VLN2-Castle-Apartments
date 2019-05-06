from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

properties = [
    {
        'name': 'cool house',
        'price': 44000000
    },
    {
        'name': 'cooler house',
        'price': 74000000
    }
]

def index(request):
    context = {'properties': properties}
    return render(request, 'realEstate/index.html', context)

def property(request):
    return HttpResponse("This will be a property listing")