from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from user.models import Profile


class UserForm(UserCreationForm):
    prefix = 'user'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': widgets.TextInput(attrs={'class': "form-control"}),
            'first_name': widgets.TextInput(attrs={'class': "form-control"}),
            'last_name': widgets.TextInput(attrs={'class': "form-control"}),
            'email': widgets.EmailInput(attrs={'class': "form-control"}),
            'password': widgets.PasswordInput(attrs={'class': "form-control"}),
            'password2': widgets.PasswordInput(attrs={'class': "form-control"}),
        }


class ProfileForm(ModelForm):
    prefix = 'profile'

    class Meta:
        model = Profile
        exclude = [ 'id', 'user' ]
        widgets = {
            'phone': widgets.TextInput(attrs={'class': "form-control", 'minlength': 7}),
            #'profileImage': widgets.FileInput(attrs={}),
        }
