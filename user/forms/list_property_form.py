from django.forms import ModelForm, widgets
from django import forms
from realEstate.models import Property, Address


# form takes in Property attributes

class AddressForm(ModelForm):
    prefix = 'address'

    class Meta:
        model = Address
        exclude = [ 'id' ]

class ListPropertyForm(ModelForm):
    prefix = 'property'

    class Meta:
        model = Property
        exclude = [ 'id', 'address', 'seller' ]
