from django.forms import ModelForm, widgets
from django import forms
from realEstate.models import Address, Property
COUNTRY_CHOICES = [()]
PRICE_CHOICES = [()]
SIZE_CHOICES = [()]
ROOM_CHOICES = [()]
TYPE_CHOICES = [()]

# class FilterForm(forms.Form):
#     country = forms.ChoiceField()
#     price_from = forms.ChoiceField()
#     price_to = forms.ChoiceField()
#     size_from = forms.ChoiceField()
#     size_to = forms.ChoiceField()
#     rooms_from = forms.ChoiceField()
#     rooms_to = forms.ChoiceField()
#     type = forms.ChoiceField()


class CountryList(ModelForm):
    class Meta:
        model = Address
        fields = ('country',)
        widgets = {
            'country': widgets.Select(attrs={'class': 'form-control'})
        }

class FilterForm(forms.Form):
    pass
