from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_list_or_404, get_object_or_404

from realEstate.models import Property, PropertyAttribute, Attribute, Address
from realEstate.forms.property_form import AddressForm, PropertyForm, PropertyImagesForm


# Create your views here.


def index(request):
    country_list = Address.objects.distinct('country')
    type_list = Property.objects.distinct('type')
    if request.is_ajax():
        filters = request.GET
        properties = [{
            'id': x.id,
            'name': x.name,
            'description': x.description,
            'type': x.type,
            'price': x.price,
            'nrBedrooms': x.nrBedrooms,
            'nrBathrooms': x.nrBathrooms,
            'squareMeters': x.squareMeters,
            'constructionYear': x.constructionYear,
            'dateCreated': x.dateCreated,
            'sold': x.sold,
            'seller': {
                'name': x.seller.first_name + ' ' + x.seller.last_name,
                'email': x.seller.email,
                'phone': x.seller.profile.phone,
            },
            'address': {
                'country': x.address.country,
                'municipality': x.address.municipality,
                'city': x.address.city,
                'postCode': x.address.postCode,
                'streetName': x.address.streetName,
                'houseNumber': x.address.houseNumber,
                'apartmentNumber': x.address.apartmentNumber,
            },
            'firstImage': (x.propertyimage_set.first().image if x.propertyimage_set.first() else ''),
            'attributes': [y for y in PropertyAttribute.objects.filter(property_id=x.id)]
        } for x in Property.objects.filter(
            name__icontains=filters.get('search_box'),
            address__country__contains=filters.get('country'),
            price__gte=filters.get('price_from'),
            price__lte=filters.get('price_to'),
            squareMeters__gte=filters.get('size_from'),
            squareMeters__lte=filters.get('size_to'),
            nrBedrooms__gte=filters.get('rooms_from'),
            nrBedrooms__lte=filters.get('rooms_to'),
            type__contains=filters.get('type')).order_by(request.GET.get('order'))]
        return JsonResponse({'data': properties})

    context = {'properties': Property.objects.order_by('name'),
               'propertiesNav': 'active',
               'country_list': country_list,
               'type_list': type_list}
    return render(request, 'realEstate/index.html', context)


def property_details(request, prop_id):
    return render(request, 'realEstate/property_details.html', {
        'property': get_object_or_404(Property, pk=prop_id),
        'propertyAttributes': PropertyAttribute.objects.filter(property_id=prop_id),
        'attributes': Attribute.objects.order_by('description')
    })

@login_required
def create(request):
    if request.method == 'POST':
        address_form = AddressForm(data=request.POST)
        property_form = PropertyForm(data=request.POST)
        image_form = PropertyImagesForm(data=request.POST)

        if property_form.is_valid() and address_form.is_valid():
            prop = property_form.save(commit=False)
            prop.seller = User.objects.get(pk=request.user.id)
            prop.address = address_form.save()
            prop.save()

            image = image_form.save(commit=False)
            image.property_id = prop.id
            image.save()
            return redirect(reverse('user-profile'))
        else:
            context = { 'address_form': address_form,
                        'property_form': property_form,
                        'image_form': image_form }
            return render(request, 'realEstate/add-property.html', context)
    else:
        context = { 'address_form': AddressForm(),
                    'property_form': PropertyForm(),
                    'image_form': PropertyImagesForm() }
        return render(request, 'realEstate/add-property.html', context)


@login_required
def update(request, prop_id):
    property_instance = Property.objects.get(pk=prop_id)
    if request.user.id != property_instance.seller.id:
        print('Seller id: ' + property_instance.seller.id + '\nUser id: ' + request.user.id)
        return redirect(reverse('user-profile'))

    property_form = PropertyForm(instance=property_instance)
    address_form = AddressForm(instance=property_instance.address)

    if request.method == 'POST':
        property_form = PropertyForm(data=request.POST, instance=property_instance)
        address_form = AddressForm(data=request.POST, instance=property_instance.address)

        #image_form = PropertyImagesForm(data=request.POST)
        if property_form.is_valid() and address_form.is_valid():
            prop = property_form.save(commit=False)
            prop.address = address_form.save()
            prop.save()

            #image = image_form.save(commit=False)
            #image.property_id = prop.id
            #image.save()
            return redirect(reverse('user-profile'))
        else:
            context = { 'pk': prop_id,
                        'address_form': address_form,
                        'property_form': property_form,
                        #'image_form': image_form,
                        }
            return render(request, 'realEstate/edit-property.html', context)
    context = {'pk': prop_id,
               'address_form': address_form,
               'property_form': property_form,
               # 'image_form': image_form,
               }
    return render(request, 'realEstate/edit-property.html', context)
