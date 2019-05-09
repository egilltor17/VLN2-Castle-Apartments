from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django import forms

from user.forms.list_property_form import ListPropertyForm, AddressForm
from realEstate.models import PropertyImage, Address

# Create your views here.


def index(request):
    context = {"sign_in": "active"}
    return render(request, 'user/index.html', context)


def profile(request):
    return render(request, 'user/profile.html', {'profile': 'active'})


def add_property(request):
    if request.method == 'POST':
        property_form = ListPropertyForm(data=request.POST)
        address_form = AddressForm(data=request.POST)
        if property_form.is_valid() and address_form.is_valid():
            prop = property_form.save(commit=False)
            seller = User.objects.get(pk=request.user.id)
            prop.seller = seller
            address = address_form.save()
            prop.address = address
            prop.save()
            return redirect(reverse('user-profile'))
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


# class UserCreateForm(UserCreationForm):
#     email = forms.CharField(max_length=100, required=True)
#      = forms.IntegerField(required=True)
#
#     class Meta:
#         model = User
#
#     def save(self, commit=True):
#         if not commit:
#             raise NotImplementedError("Can't create User and UserProfile without database save")
#         user = super(UserCreateForm, self).save(commit=True)
#         user_profile = UserProfile(user=user, email=self.cleaned_data['job_title'],
#             age=self.cleaned_data['age'])
#         user_profile.save()
#         return user, user_profile


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
