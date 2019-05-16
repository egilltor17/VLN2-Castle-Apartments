from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from miscellaneous.forms.payment_form import PurchaseForm, PaymentInfoForm
from realEstate.forms.property_form import AddressForm
from realEstate.models import Property
from user.models import Purchase


def home(request):
    return redirect('property-index')


def about_us(request):
    context = {"about_us": "active"}
    return render(request, 'miscellaneous/aboutUs.html', context)


@login_required
def purchase(request, prop_id):
    address_form = AddressForm(data=request.POST)
    card_info_form = PaymentInfoForm(data=request.POST)
    purchase_form = PurchaseForm(data=request.POST)
    if request.method == 'POST':
        if address_form.is_valid() and card_info_form.is_valid() and purchase_form.is_valid():
            prop = Property.objects.get(pk=prop_id)
            prop.sold = True
            prop.save()

            card = card_info_form.save(commit=False)
            address = address_form.save(commit=False)
            address.country = request.POST['country-list']
            address.save()
            card.address = address
            card.save()

            pur = purchase_form.save(commit=False)
            pur.paymentInfo_id = card.id
            pur.property_id = prop_id
            pur.userInfo_id = request.user.id
            pur.save()
            return redirect('review/' + str(pur.pk))
    context = { 'property': get_object_or_404(Property, pk=prop_id),
                'address_form': address_form,
                'card_info_form': card_info_form,
                'purchase_form': purchase_form, }
    return render(request, 'miscellaneous/purchase.html', context)


@login_required
def purchase_review(request, pur_id):
    purchase_instance = Purchase.objects.get(pk=pur_id)
    if request.user.id != purchase_instance.userInfo.id:
        return redirect('user-profile')
    context = { 'purchase': purchase_instance,
                'property': purchase_instance.property,}
    return render(request, 'miscellaneous/purchase-review.html', context)


def error_404(request, exception=None):
    return render(request, 'miscellaneous/error_404.html')


def error_500(request, exception=None):
    return render(request, 'miscellaneous/error_500.html')
