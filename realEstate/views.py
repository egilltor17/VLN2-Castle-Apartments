from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from realEstate.models import Property, PropertyAttribute, Attribute, Address
from realEstate.forms.filter_form import FilterForm
from user.forms.recently_viewed_form import RecentlyViewedForm
from datetime import datetime

# Create your views here.
from user.models import RecentlyViewed


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
            name__contains=filters.get('search_box'),
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


def property_details(request, id):
    property = get_object_or_404(Property, pk=id)
    if request.user.is_authenticated:
        recently_viewed = RecentlyViewed()
        recently_viewed.timestamp = datetime.now()
        recently_viewed.property = property
        recently_viewed.user = request.user
        recently_viewed.save()

    return render(request, 'realEstate/property_details.html', {
            'property': property,
            'propertyAttributes': PropertyAttribute.objects.filter(property_id=id),
            'attributes': Attribute.objects.order_by('description')
        })


@login_required
def create():
    return 0


@login_required
def update():
    return 0
