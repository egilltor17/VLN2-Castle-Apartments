from django.forms import ModelForm, widgets
from realEstate.models import Address, Property, PropertyImage

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


class PropertyFormNone(ModelForm):
    prefix = 'property'

    class Meta:
        model = Property
        exclude = [ 'id',
                    'name',
                    'description',
                    'type',
                    'price',
                    'nrBedrooms',
                    'nrBathrooms',
                    'squareMeters',
                    'constructionYear',
                    'dateCreated',
                    'sold',
                    'address',
                    'seller',
                    'image' ]


class PropertyImagesForm(ModelForm):
    prefix = 'property-image'

    class Meta:
        model = PropertyImage
        exclude = [ 'id', 'property' ]
