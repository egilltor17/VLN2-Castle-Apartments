from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse
from django.db.models import Case, When

from realEstate.models import Property, Address
from user.models import Profile, RecentlyViewed, Favorites, Purchase
from user.forms.registration_form import ProfileForm, UserForm
# Create your views here.


@login_required
def profile(request):
    # Get all recently viewed properties for the user logged in
    pks = [rec.property_id for rec in RecentlyViewed.objects.filter(user_id=request.user.id).order_by('-timestamp')]
    # To hold the order by timestamp
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
    recently_viewed_properties = Property.objects.filter(pk__in=pks).order_by(preserved)[:10]

    # Get all favorites for the user logged in
    pks2 = [fav.property_id for fav in Favorites.objects.filter(user_id=request.user.id)]
    favorites = Property.objects.filter(pk__in=pks2)

    # Get all purchased properties for the user logged in
    purchased_properties = Purchase.objects.filter(userInfo_id=request.user.id)

    context = {'properties': Property.objects.filter(seller=request.user).order_by('-dateCreated'),
               'recently_viewed_properties': recently_viewed_properties,
               'favorites': favorites,
               'purchased_properties': purchased_properties}
    return render(request, 'user/profile.html', context)


def seller_profile(request, user_id):
    if request.user.id == user_id:
        return redirect('user-profile')
    context = {'properties': Property.objects.filter(seller__pk=user_id).order_by('-dateCreated'),
               'seller': User.objects.get(pk=user_id)}
    return render(request, 'user/sellerProfile.html', context)


@login_required
def edit_profile(request):
    profile_instance = Profile.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        profile_form = ProfileForm(instance=profile_instance, data=request.POST, files=request.FILES)
        user_form = UserForm(instance=request.user, data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            prof = profile_form.save(commit=False)
            prof.profileImage = (prof.profileImage if prof.profileImage else 'profileImages/user.png')
            prof.save()
            user_form.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('user-profile')
        else:
            context = {'profile_form': profile_form, 'user_form': user_form}
            return render(request, 'user/edit-profile.html', context)
    else:
        context = {'profile_form': ProfileForm(instance=profile_instance),
                   'user_form': UserForm(instance=request.user),}
        return render(request, 'user/edit-profile.html', context)


def register(request):
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        user_form = UserForm(data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            prof = profile_form.save(commit=False)
            prof.profileImage = (prof.profileImage if prof.profileImage else 'profileImages/user.png')
            prof.user = user_form.save()
            prof.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect(reverse('user-profile'))
        else:
            context = {'profile_form': profile_form, 'user_form': user_form}
            return render(request, 'user/register.html', context)
    else:
        context = {'profile_form': ProfileForm(), 'user_form': UserForm()}
        return render(request, 'user/register.html', context)
