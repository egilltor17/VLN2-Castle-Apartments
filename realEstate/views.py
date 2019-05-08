from django.shortcuts import render, get_list_or_404, get_object_or_404
from realEstate.models import Property, PropertyAttribute, Attribute
from realEstate.forms.filter_form import *
from django.
# Create your views here.


def index(request):
    context = {'properties': Property.objects.order_by('name')}
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
