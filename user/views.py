from django.shortcuts import render, redirect
from django.http import HttpResponse

from user.forms.list_property_form import ListPropertyForm
from realEstate.models import PropertyImage, Address

# Create your views here.


def index(request):
    return render(request, 'user/index.html')

def profile(request):
    return HttpResponse("This will be a profile page")

def list_property(request):
    if request.method == 'POST':
        form = ListPropertyForm(data=request.POST)
        if form.is_valid():
            prop = form.save()
            prop_image = PropertyImage(image=request.POST['image'], property=prop)
            prop_image.save()
            #prop_address = Address(data=request.POST)
            #prop_address.save()
            return redirect('user-index')
    else:
        form = ListPropertyForm()
    return render(request, 'user/list_property.html', {
        'form': form
    })