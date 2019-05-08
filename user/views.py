from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    context = {"signin": "active"}
    return render(request, 'user/index.html', context)


def profile(request):
    return render(request, 'user/profile.html', {'profile': 'active'})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'user/register.html', {
        'register': 'active',
        'form': UserCreationForm()
    })


@login_required
def create_property(request):
    return render(request, 'user/create_property.html')