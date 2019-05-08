from django.http import JsonResponse
from django.shortcuts import render, get_list_or_404, get_object_or_404
from realEstate.models import Property, PropertyAttribute, Attribute
from realEstate.forms.filter_form import *
# Create your views here.


def index(request):
    if 'search_filter' in request.GET:
        search_filter = request.GET['search_filter']
        properties = [{
            'id':  x.id,
            'name': x.name,
            'description': x.description,
            'type': x.type,
            'price': x.price,
            'nrBedrooms': x.nrBedrooms,
            'nrBathrooms': x.nrBathrooms,
            'squareMeters': x.squareMeters,
            'constructionYear': x.constructionYear,
            'sellerName': x.sellerName,
            'sellerEmail': x.sellerEmail,
            'sellerPhone': x.sellerPhone,
            'dateCreated': x.dateCreated,
            # 'sold': x.sold,
            'address': {
                'country': x.address.country,
                'municipality': x.address.municipality,
                'city': x.address.city,
                'postCode': x.address.postCode,
                'streetName': x.address.streetName,
                'houseNumber': x.address.houseNumber,
                'apartmentNumber': x.address.apartmentNumber,
            },
            'firstImage': x.propertyimage_set.first().image
        } for x in Property.objects.filter(name__icontains=search_filter)]
        return JsonResponse({'data': properties})
    context = {'properties': Property.objects.order_by('name'), "propertiesNav": "active"}
    return render(request, 'realEstate/index.html', context)


def property_details(request, id):
    return render(request, 'realEstate/property_details.html', {
        'property': get_object_or_404(Property, pk=id),
        'propertyAttributes': PropertyAttribute.objects.filter(property_id=id),
        'attributes': Attribute.objects.order_by('description')
    })

def filter(request):
    form = FilterForm()
    return render(request, 'realEstate/index.html', {
        'form': form
    })
