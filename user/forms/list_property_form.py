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
        exclude = [ 'id', 'address' ]
        #model = Address
        #fields = ['__all__']

    #image = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #address = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    #address = forms.Form()

    #class Meta:
   #     model = Property
    #    exclude = ['id']
     #   widgets = {
      #      'name': widgets.TextInput(attrs={'class': 'form-control'}),
       #     'description': widgets.TextInput(attrs={'class': 'form-control'}),
        #    'type': widgets.TextInput(attrs={'class': 'form-control'}),
         #   'price': widgets.NumberInput(attrs={'class': 'form-control'}),
     #       'nrBedrooms': widgets.NumberInput(attrs={'class': 'form-control'}),
      #      'nrBathrooms': widgets.NumberInput(attrs={'class': 'form-control'}),
       #     'squareMeters': widgets.NumberInput(attrs={'class': 'form-control'}),
        #    'constructionYear': widgets.NumberInput(attrs={'class': 'form-control'}),
         #   # seller = models.ForeignKey(User, on_delete=models.CASCADE)
        #    'sellerName': widgets.TextInput(attrs={'class': 'form-control'}),
         #   'sellerEmail': widgets.TextInput(attrs={'class': 'form-control'}),
          #  'sellerPhone': widgets.TextInput(attrs={'class': 'form-control'}),
        #    'dateCreated': widgets.TextInput(attrs={'class': 'form-control'}),
        #    'sold': widgets.TextInput(attrs={'class': 'form-control'}),
       # }

'''
            'address': {
                'country': widgets.TextInput(attrs={'class': 'form-control'}),
                'municipality': widgets.TextInput(attrs={'class': 'form-control'}),
                'city': widgets.TextInput(attrs={'class': 'form-control'}),
                'postCode': widgets.TextInput(attrs={'class': 'form-control'}),
                'streetName': widgets.TextInput(attrs={'class': 'form-control'}),
                'houseNumber': widgets.TextInput(attrs={'class': 'form-control'}),
                'apartmentNumber': widgets.TextInput(attrs={'class': 'form-control'}),
            },
'''