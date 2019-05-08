from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context = {"signin": "active"}
    return render(request, 'user/index.html', context)

def profile(request):
    return  HttpResponse("This will be a profile page")

def create_property(request):
    return render(request, 'user/create_property.html')