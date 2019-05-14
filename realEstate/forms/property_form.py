from django.forms import ModelForm, widgets
from realEstate.models import Address, Attribute, Property, PropertyImage

# form takes in Property attributes


class AddressForm(ModelForm):
    prefix = 'address'

    class Meta:
        model = Address
        exclude = [ 'id' ]


class PropertyForm(ModelForm):
    prefix = 'property'

    class Meta:
        model = Property
        exclude = [ 'id', 'address', 'seller', 'dateCreated', 'sold' ]


class PropertyImagesForm(ModelForm):
    prefix = 'property-image'

    class Meta:
        model = PropertyImage
        exclude = [ 'id', 'property' ]


class AttributeForm(ModelForm):
    prefix = 'property-attribute'

    class Meta:
        model = Attribute
        exclude = [ 'id', 'property' ]