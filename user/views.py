from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.utils import timezone

from user.forms.registration_form import CustomUserCreateForm, ProfileForm, UserForm
from user.forms.list_property_form import ListPropertyForm, AddressForm

# Create your views here.


def profile(request):
    return render(request, 'user/profile.html', {'profile': 'active'})


@login_required
def add_property(request):
    if request.method == 'POST':
        property_form = ListPropertyForm(data=request.POST)
        address_form = AddressForm(data=request.POST)
        if property_form.is_valid() and address_form.is_valid():
            prop = property_form.save(commit=False)
            prop.seller = User.objects.get(pk=request.user.id)
            prop.address = address_form.save()
            prop.save()
            return redirect(reverse('user-profile'))
        else:
            context = {'property_form': property_form, 'address_form': address_form}
            return render(request, 'user/add-property.html', context)
    else:
        context = {'property_form': ListPropertyForm(), 'address_form': AddressForm()}
        return render(request, 'user/add-property.html', context)

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


def register(request):
    # if request.method == 'POST':
    #     registration_form = CustomUserCreateForm(data=request.POST)
    #     if registration_form.is_valid():
    #         registration_form.save()
    #         return redirect('login')
    # return render(request, 'user/register.html', {
    #     'register': 'active',
    #     'registration_form': CustomUserCreateForm()
    # })




    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST)
        user_form = UserForm(data=request.POST)
        print('hello world')
        if profile_form.is_valid() and user_form.is_valid():
            prof = profile_form.save(commit=False)
            user = user_form.save()
            user.last_login = timezone.now()
            user.is_superuser = False
            user.is_staff = False
            user.is_active = True
            user.date_joined = timezone.now()
            user.groups = ['']
            user.user_permissions = ['']
            prof.user = user
            prof.save()
            return redirect(reverse('login'))

            # prop = property_form.save(commit=False)
            # prop.seller = User.objects.get(pk=request.user.id)
            # prop.address = address_form.save()
            # prop.save()
        else:
            context = {'profile_form': profile_form, 'user_form': user_form}
            return render(request, 'user/register.html', context)
    else:
        context = {'profile_form': ProfileForm(), 'user_form': UserForm()}
        return render(request, 'user/register.html', context)
