from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django import forms

# Create your views here.


def index(request):
    context = {"sign_in": "active"}
    return render(request, 'user/index.html', context)


def profile(request):
    return render(request, 'user/profile.html', {'profile': 'active'})


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