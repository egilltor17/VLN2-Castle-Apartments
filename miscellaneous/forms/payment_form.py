from django.forms import ModelForm, widgets
from user.models import PaymentInfo, Purchase


class PaymentInfoForm(ModelForm):
    prefix = 'payment'

    class Meta:
        model = PaymentInfo
        exclude = [ 'id', 'address' ]


class PurchaseForm(ModelForm):
    prefix = 'purchase'

    class Meta:
        model = Purchase
        exclude = [ 'id', 'paymentInfo', 'property', 'userInfo', 'date' ]

