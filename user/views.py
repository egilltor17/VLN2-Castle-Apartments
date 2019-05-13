from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, reverse

from user.forms.registration_form import ProfileForm, UserForm

from user.models import Profile
# Create your views here.


@login_required
def profile(request):
    return render(request, 'user/profile.html', {'profile': 'active',})


@login_required
def editProfile(request):
    profileInstance = Profile.objects.filter(user=request.user).first()
    if request.method == 'POST':
        profile_form = ProfileForm(instance=profileInstance, data=request.POST, files=request.FILES)
        user_form = UserForm(instance=request.user, data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('user-profile')
    return render(request, 'user/editProfile.html', {
        'profile': 'active',
        'profile_form': ProfileForm(instance=profileInstance),
        'user_form': UserForm(instance=request.user)
    })


def register(request):
    if request.method == 'POST':
        profile_form = ProfileForm(data=request.POST, files=request.FILES)
        user_form = UserForm(data=request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            prof = profile_form.save(commit=False)
            print(prof.profileImage)
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
