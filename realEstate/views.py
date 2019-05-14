from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import modelformset_factory, inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from datetime import datetime

from realEstate.forms.property_form import AddressForm, PropertyForm
from realEstate.models import Property, PropertyImage, Attribute, Address  #, PropertyAttribute
from user.models import RecentlyViewed, Favorites

def index(request):
    country_list = Address.objects.distinct('country')
    municipality_list = Address.objects.distinct('municipality')
    city_list = Address.objects.distinct('city')
    postcode_list = Address.objects.distinct('postCode')
    type_list = Property.objects.distinct('type')
    year_built_list = Property.objects.distinct('constructionYear')
    attribute_list = Attribute.objects.distinct('description')

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
            #'attributes': [y.id for y in PropertyAttribute.objects.filter(property_id=x.id)]
            #'attributes': x.attributes,
        } for x in Property.objects.prefetch_related('propertyimage_set').select_related('seller__profile', 'address').filter(
            name__icontains=filters.get('search_box'),
            address__country__contains=filters.get('country'),
            address__municipality__contains=filters.get('municipality'),
            address__city__contains=filters.get('city'),
            address__postCode__contains=filters.get('postcode'),
            price__gte=filters.get('price_from'),
            price__lte=filters.get('price_to'),
            squareMeters__gte=filters.get('size_from'),
            squareMeters__lte=filters.get('size_to'),
            nrBedrooms__gte=filters.get('bedrooms_from'),
            nrBedrooms__lte=filters.get('bedrooms_to'),
            nrBathrooms__gte=filters.get('bathrooms_from'),
            nrBathrooms__lte=filters.get('bathrooms_to'),
            constructionYear__gte=filters.get('year_built_from'),
            constructionYear__lte=filters.get('year_built_to'),
            type__contains=filters.get('type')).order_by(request.GET.get('order'))]
        return JsonResponse({'data': properties})

    context = {'properties': Property.objects.order_by('name'),
               'propertiesNav': 'active',
               'country_list': country_list,
               'municipality_list': municipality_list,
               'city_list': city_list,
               'postcode_list': postcode_list,
               'type_list': type_list,
               'year_built_list': year_built_list,
               'attribute_list': attribute_list}
    return render(request, 'realEstate/index.html', context)


def property_details(request, prop_id):
    property = get_object_or_404(Property, pk=prop_id)
    is_favorite = False
    if request.user.is_authenticated:
        recently_viewed = RecentlyViewed()
        recently_viewed.timestamp = datetime.now()
        recently_viewed.property = property
        recently_viewed.user = request.user
        recently_viewed.save()
        if Favorites.objects.filter(property_id=property.id).filter(user_id=request.user).count() == 0:
            is_favorite = False
        else:
            is_favorite = True
    return render(request, 'realEstate/property_details.html', {
            'property': property,
            #'propertyAttributes': PropertyAttribute.objects.filter(property_id=prop_id),
            'attributes': Attribute.objects.order_by('description'),
            'is_favorite': is_favorite
        })

@login_required()
def favorite_property(request, prop_id):
    property = get_object_or_404(Property, pk=prop_id)
    favorite = Favorites()
    favorite.property = property
    favorite.user = request.user
    favorite.save()
    return redirect('property-details', prop_id)


@login_required()
def unfavorite_property(request, prop_id):
    favorite = get_object_or_404(Favorites, property_id=prop_id, user_id=request.user)
    favorite.delete()
    return redirect('property-details', prop_id)


@login_required
def create(request):
    images_form_set = modelformset_factory(PropertyImage, fields=('image',), extra=5)
    if request.method == 'POST':
        address_form = AddressForm(data=request.POST)
        property_form = PropertyForm(data=request.POST)
        image_form = images_form_set(data=request.POST)

        if property_form.is_valid() and address_form.is_valid() and image_form.is_valid():
            prop = property_form.save(commit=False)
            prop.seller = User.objects.get(pk=request.user.id)
            prop.address = address_form.save()
            prop.save()

            images = image_form.save(commit=False)
            for image in images:
                image.property_id = prop.id
                image.save()

            return redirect(reverse('user-profile'))
        else:
            context = { 'address_form': address_form,
                        'property_form': property_form,
                        'image_form': image_form, }
            return render(request, 'realEstate/add-property.html', context)
    else:
        context = { 'address_form': AddressForm(),
                    'property_form': PropertyForm(),
                    'image_form': images_form_set(queryset=PropertyImage.objects.none()), }
        return render(request, 'realEstate/add-property.html', context)


@login_required
def update(request, prop_id):
    property_instance = Property.objects.get(pk=prop_id)
    images_form_set = inlineformset_factory(Property, PropertyImage, fields=('image',))
    if request.user.id != property_instance.seller.id:
        print('Seller id: ' + property_instance.seller.id + '\nUser id: ' + request.user.id)
        return redirect(reverse('user-profile'))

    if request.method == 'POST':
        property_form = PropertyForm(data=request.POST, instance=property_instance)
        address_form = AddressForm(data=request.POST, instance=property_instance.address)
        image_form = images_form_set(data=request.POST, instance=property_instance)

        if property_form.is_valid() and address_form.is_valid() and image_form.is_valid():
            prop = property_form.save(commit=False)
            prop.address = address_form.save()
            prop.save()

            image_form.save()
            return redirect(reverse('user-profile'))
        else:
            context = { 'pk': prop_id,
                        'address_form': address_form,
                        'property_form': property_form,
                        'image_form': image_form, }
            return render(request, 'realEstate/edit-property.html', context)
    context = {'pk': prop_id,
               'address_form': AddressForm(instance=property_instance.address),
               'property_form': PropertyForm(instance=property_instance),
               'image_form': images_form_set(instance=property_instance), }
    return render(request, 'realEstate/edit-property.html', context)
