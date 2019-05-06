from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello from the index function within the user app")

def profile(request):
    return  HttpResponse("This will be a profile page")