from django.shortcuts import render, redirect
from django.http import HttpResponse

from user.forms.list_property_form import ListPropertyForm, AddressForm
from realEstate.models import PropertyImage, Address

# Create your views here.


def index(request):
    return render(request, 'user/index.html')

def profile(request):
    return HttpResponse("This will be a profile page")

def add_property(request):
    if request.method == 'POST':
        property_form = ListPropertyForm(data=request.POST)
        address_form = AddressForm(data=request.POST)
        if property_form.is_valid() and address_form.is_valid():
            prop = property_form.save(commit=False)
            address = address_form.save()
            prop.address = address
            prop.save()
        else:
            context = {'property_form': property_form, 'address_form': address_form}
            return render(request, 'user/add_property.html', context)
    else:
        context = {'property_form': ListPropertyForm(), 'address_form': AddressForm()}
        return render(request, 'user/add_property.html', context)

#def list_property(request):
#    if request.method == 'POST':
#        form = ListPropertyForm(data=request.POST)
#        if form.is_valid():
#            prop = form.save()
#            prop_image = PropertyImage(image=request.POST['image'], property=prop)
#            prop_image.save()
            #prop_address = Address(data=request.POST)
            #prop_address.save()
#            return redirect('user-index')
#    else:
#        form = ListPropertyForm()
#    return render(request, 'user/list_property.html', {
#        'form': form
#    })