from django.forms import ModelForm, widgets
from realEstate.models import Address, Attribute, Property, PropertyImage

# form takes in Property attributes


class AddressForm(ModelForm):
    prefix = 'address'

    class Meta:
        model = Address
        exclude = [ 'id', 'country' ]
        widgets = {
            'municipality': widgets.TextInput(attrs={'class': 'form-control'}),
            'city': widgets.TextInput(attrs={'class': 'form-control'}),
            'postCode': widgets.TextInput(attrs={'class': 'form-control'}),
            'streetName': widgets.TextInput(attrs={'class': 'form-control'}),
            'houseNumber': widgets.TextInput(attrs={'class': 'form-control'}),
            'apartmentNumber': widgets.TextInput(attrs={'class': 'form-control'}),
        }


class PropertyForm(ModelForm):
    prefix = 'property'

    class Meta:
        model = Property
        exclude = [ 'id', 'address', 'seller', 'dateCreated', 'sold' ]
        widgets = {
            'name': widgets.TextInput(attrs={'class': 'form-control'}),
            'description': widgets.Textarea(attrs={'class': 'form-control'}),
            'type': widgets.TextInput(attrs={'class': 'form-control'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '999999999999'}),
            'nrBedrooms': widgets.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '999999999999'}),
            'nrBathrooms': widgets.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '999999999999'}),
            'squareMeters': widgets.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '999999999999'}),
            'constructionYear': widgets.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '999999999999'}),
            'attributes': widgets.CheckboxSelectMultiple(attrs={}),
        }


class PropertyImagesForm(ModelForm):
    prefix = 'property-image'

    class Meta:
        model = PropertyImage
        exclude = [ 'id', 'property' ]
        widgets = {
            'image': widgets.TextInput(attrs={'class': 'form-control'}),
        }
