from django.shortcuts import render

# Create your views here.


def about_us(request):
    return render(request, 'miscellaneous/aboutUs.html')


def home(request):
    return render(request, 'miscellaneous/home.html')
