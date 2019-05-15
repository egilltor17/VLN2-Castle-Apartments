from django.forms import ModelForm, widgets
from django import forms
from realEstate.models import Address, Property

class FilterForm(forms.Form):
    country = forms.ChoiceField()
    price_from = forms.DecimalField(label_suffix=' (USD):')
    price_to = forms.DecimalField(label_suffix=' (USD):')
    size_from = forms.DecimalField(label_suffix=' (m²):')
    size_to = forms.DecimalField(label_suffix=' (m²):')
    rooms_from = forms.DecimalField()
    rooms_to = forms.DecimalField()
    type = forms.ChoiceField()



