from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from user.models import Profile

# Work in progress
class CustomUserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=254, required=True)
    phone = forms.CharField(max_length=32, required=False)
    image = forms.ImageField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreateForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        # user.profile.phone = self.cleaned_data["phone"]
        # user.profile.profileImage = self.cleaned_data["image"]
        if commit:
            user.save()
        return user


class UserForm(ModelForm):
    prefix = 'user'

    class Meta:
        model = User
        exclude = [ 'id',
                    'last_login',
                    'is_superuser',
                    'is_staff',
                    'is_active',
                    'date_joined',
                    'groups',
                    'user_permissions' ]


class ProfileForm(ModelForm):
    prefix = 'profile'

    class Meta:
        model = Profile
        exclude = [ 'id', 'user' ]
