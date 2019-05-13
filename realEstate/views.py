from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from realEstate.models import Property, PropertyAttribute, Attribute, Address



# Create your views here.

def index(request):
    country_list = Address.objects.distinct('country')
    municipality_list = Address.objects.distinct('municipality')
    city_list = Address.objects.distinct('city')
    postcode_list = Address.objects.distinct('postCode')
    type_list = Property.objects.distinct('type')
    year_built_list = Property.objects.distinct('constructionYear')
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
               'year_built_list': year_built_list}
    return render(request, 'realEstate/index.html', context)


def property_details(request, id):
    return render(request, 'realEstate/property_details.html', {
        'property': get_object_or_404(Property, pk=id),
        'propertyAttributes': PropertyAttribute.objects.filter(property_id=id),
        'attributes': Attribute.objects.order_by('description')
    })


@login_required
def create():
    return 0


@login_required
def update():
    return 0
