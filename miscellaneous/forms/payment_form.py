from django.forms import ModelForm, widgets
from user.models import PaymentInfo, Purchase


class PaymentInfoForm(ModelForm):
    prefix = 'payment'

    class Meta:
        model = PaymentInfo
        exclude = [ 'id', 'address' ]
        widgets = {
            'cardNumber': widgets.TextInput(attrs={ 'class': 'form-control', 'pattern': '\d*', 'minlength': 16, 'maxlength': 16 }),
            'cardName': widgets.TextInput(attrs={ 'class': 'form-control' }),
            'cardCVC': widgets.TextInput(attrs={ 'class': 'form-control', 'minlength': 3, 'maxlength': 3 }),
            'cardExpiryMonth': widgets.NumberInput(attrs={ 'class': 'form-control', 'min': 1, 'max': 12 }),
            'cardExpiryYear': widgets.NumberInput(attrs={ 'class': 'form-control', 'min': 19, 'max': 99 }),
        }


class PurchaseForm(ModelForm):
    prefix = 'purchase'

    class Meta:
        model = Purchase
        exclude = [ 'id', 'paymentInfo', 'property', 'userInfo', 'date' ]
        widgets = {
            'SSN': widgets.NumberInput(attrs={'class': 'form-control', 'minlenght': 10})
        }



