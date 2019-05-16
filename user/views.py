from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse
from django.db.models import Case, When

from realEstate.models import Property, Address
from user.models import Profile, RecentlyViewed, Favorites
from user.forms.registration_form import ProfileForm, UserForm
# Create your views here.


@login_required
def profile(request):

    pks = [recently_viewed.property_id for recently_viewed in RecentlyViewed.objects.filter(user_id=request.user.id).order_by('-timestamp')]
    # To hold the order by timestamp
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pks)])
    properties = Property.objects.filter(pk__in=pks).order_by(preserved)[:10]

    #Get all favorites for the user logged in
    pks2 = [favorite.property_id for favorite in Favorites.objects.filter(user_id=request.user.id)]
    #Get all properties that are favorited by the user logged in
    favorites = Property.objects.filter(pk__in=pks2)

    context = {'properties': Property.objects.filter(seller=request.user).order_by('-dateCreated'),
               'profile': 'active',
               'recently_viewed_properties': properties,
               'favorites': favorites}
    return render(request, 'user/profile.html', context)


def view_other_profiles(request, user_id):
    context = {'properties': Property.objects.filter(seller__pk=user_id).order_by('-dateCreated'),
               'seller': User.objects.get(pk=user_id)}
    if request.user.id == user_id:
        return redirect('user-profile')
    return render(request, 'user/sellerProfile.html', context)


@login_required
def editProfile(request):
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
            return render(request, 'user/editProfile.html', context)
    return render(request, 'user/editProfile.html', {
        'profile': 'active',
        'profile_form': ProfileForm(instance=profile_instance),
        'user_form': UserForm(instance=request.user)
    })


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
