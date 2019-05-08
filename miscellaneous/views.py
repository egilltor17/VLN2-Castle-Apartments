from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'miscellaneous/home.html')

def about_us(request):
    context = {"about_us": "active"}
    return render(request, 'miscellaneous/aboutUs.html', context)


