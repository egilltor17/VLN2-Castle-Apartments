from django.shortcuts import render
from django.http import HttpResponse  # legacy
from realEstate.models import Property

# Create your views here.


def index(request):
    context = {'properties': Property.objects.order_by('name')}
    return render(request, 'realEstate/index.html', context)

def property(request):
    return HttpResponse("This will be a property listing")