from django.forms import ModelForm, widgets
from django import forms
from user.models import RecentlyViewed

class RecentlyViewedForm(ModelForm):
    class Meta:
        model = RecentlyViewed
        exclude = ['id', 'timestamp', 'property_id', 'user_id']