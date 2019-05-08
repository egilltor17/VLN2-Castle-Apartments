from django.forms import ModelForm, widgets
from django import forms
from realEstate.models import Property

class FilterForm:
    class Meta:
        model = Property
        exclude = ['id']
        widgets = {
            'country': widgets.ChoiceWidget(attrs={'class': 'form-control'}),
            'price from': widgets.ChoiceWidget(attrs={'class': 'form-control'}),
            'price to': widgets.ChoiceWidget(attrs={'class': 'form-control'}),
            'size from': widgets.ChoiceWidget(attrs={'class': 'form-control'}),
            'size to': widgets.ChoiceWidget(attrs={'class': 'form-control'}),
            'rooms from': widgets.ChoiceWidget(attrs={'class': 'form-control'}),
            'rooms to': widgets.ChoiceWidget(attrs={'class': 'form-control'}),
            'type': widgets.ChoiceWidget(attrs={'class': 'form-control'}),

        }