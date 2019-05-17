from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.forms import modelformset_factory, inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from datetime import datetime

from realEstate.forms.property_form import AddressForm, PropertyForm
from realEstate.models import Property, PropertyImage, Attribute
from user.models import RecentlyViewed, Favorites


def property_to_json(property):
    return {'id': property.id,
            'name': property.name,
            'description': property.description,
            'type': property.type,
            'price': property.price,
            'nrBedrooms': property.nrBedrooms,
            'nrBathrooms': property.nrBathrooms,
            'squareMeters': property.squareMeters,
            'constructionYear': property.constructionYear,
            'dateCreated': property.dateCreated,
            'sold': property.sold,
            'seller': {
                'name': property.seller.first_name + ' ' + property.seller.last_name,
                'email': property.seller.email,
                'phone': property.seller.profile.phone,
            },
            'address': {
                'country': property.address.country,
                'municipality': property.address.municipality,
                'city': property.address.city,
                'postCode': property.address.postCode,
                'streetName': property.address.streetName,
                'houseNumber': property.address.houseNumber,
                'apartmentNumber': property.address.apartmentNumber,
            },
            'firstImage': (property.propertyimage_set.first().image if property.propertyimage_set.first() else ''),
            'attributes': [y.description for y in property.attributes.all()],
    }


def index(request):
    # Pre fetching data from the database
    property_db = Property.objects.filter(sold=False).prefetch_related('propertyimage_set').select_related('seller__profile', 'address')

    # Initial values for the form
    country_list = property_db.distinct('address__country')
    municipality_list = property_db.none()
    city_list = property_db.none()
    postcode_list = property_db.none()
    type_list = property_db.distinct('type')
    year_built_list = property_db.distinct('constructionYear')
    attribute_list = Attribute.objects.distinct('description')

    # Load all municipalities & cities for a country to pre populate their drop downs
    if request.is_ajax() and 'enable_municipalities' in request.GET:
        municipalities = property_db.filter(address__country__contains=request.GET.get('country')).distinct('address__municipality')
        municipality_list = [x.address.municipality for x in municipalities]
        cities = property_db.filter(address__country__contains=request.GET.get('country')).distinct('address__city')
        city_list = [x.address.city for x in cities]
        postcodes = property_db.filter(address__country__contains=request.GET.get('country')).distinct('address__postCode')
        postcode_list = [x.address.postCode for x in postcodes]
        return JsonResponse({'data': {'municipalities': municipality_list, 'cities': city_list, 'postcodes': postcode_list}})
    # Load all cities for a country & municipalities to pre populate its drop down
    if request.is_ajax() and 'enable_cities' in request.GET:
        cities = property_db.filter(address__municipality__contains=request.GET.get('municipality')).distinct('address__city')
        city_list = [x.address.city for x in cities]
        return JsonResponse({'data': city_list})

    # Load all postcodes for a country & municipalities to pre populate its drop down
    if request.is_ajax() and 'enable_postcodes' in request.GET:
        postcodes = property_db.filter(address__city__contains=request.GET.get('city')).distinct('address__postCode')
        postcode_list = [x.address.postCode for x in postcodes]
        return JsonResponse({'data': postcode_list})

    # Load all properties on first load
    if request.is_ajax() and 'initial_filter' in request.GET:
        properties = [property_to_json(x) for x in property_db.order_by('-dateCreated')]
        return JsonResponse({'data': properties})

    # Filters the properties with the parameters form the filter form
    if request.is_ajax() and 'search_box' in request.GET:
        # All attributes
        attr_query_set = [x for x in request.GET if x.isdigit()]
        filters = request.GET

        if attr_query_set:
            # Filters with search and attribute checkboxes
            properties = [property_to_json(x) for x in property_db.filter(
                # Giant filter query using all the elements of the filter form
                Q(name__icontains=filters.get('search_box')) |
                Q(description__icontains=filters.get('search_box')),
                Q(address__country__contains=filters.get('country')),
                # To avoid none values for municipalities in the query string
                ( Q(address__municipality__contains=filters.get('municipality')) |
                  Q(address__municipality__isnull=True)
                  if filters.get('municipality') == "" else
                  Q(address__municipality__contains=filters.get('municipality')) ),
                Q(address__city__contains=filters.get('city')),
                Q(address__postCode__contains=filters.get('postcode')),
                Q(price__gte=filters.get('price_from')),
                Q(price__lte=filters.get('price_to')),
                Q(squareMeters__gte=filters.get('size_from')),
                Q(squareMeters__lte=filters.get('size_to')),
                Q(nrBedrooms__gte=filters.get('bedrooms_from')),
                Q(nrBedrooms__lte=filters.get('bedrooms_to')),
                Q(nrBathrooms__gte=filters.get('bathrooms_from')),
                Q(nrBathrooms__lte=filters.get('bathrooms_to')),
                Q(constructionYear__gte=filters.get('year_built_from')),
                Q(constructionYear__lte=filters.get('year_built_to')),
                Q(type__contains=filters.get('type'))
            ).filter(attributes__id__in=attr_query_set).annotate(num_attributes=Count('attributes')
            ).filter(num_attributes=len(attr_query_set)).order_by(request.GET.get('order'))]
        else:
            # Filters with search and without attribute checkboxes
            properties = [property_to_json(x) for x in property_db.filter(
                # Giant filter query using all the elements of the filter form
                Q(name__icontains=filters.get('search_box')) |
                Q(description__icontains=filters.get('search_box')),
                Q(address__country__contains=filters.get('country')),
                # To avoid none values for municipalities in the query string
                ( Q(address__municipality__contains=filters.get('municipality')) |
                  Q(address__municipality__isnull=True)
                  if filters.get('municipality') == "" else
                  Q(address__municipality__contains=filters.get('municipality')) ),
                Q(address__city__contains=filters.get('city')),
                Q(address__postCode__contains=filters.get('postcode')),
                Q(price__gte=filters.get('price_from')),
                Q(price__lte=filters.get('price_to')),
                Q(squareMeters__gte=filters.get('size_from')),
                Q(squareMeters__lte=filters.get('size_to')),
                Q(nrBedrooms__gte=filters.get('bedrooms_from')),
                Q(nrBedrooms__lte=filters.get('bedrooms_to')),
                Q(nrBathrooms__gte=filters.get('bathrooms_from')),
                Q(nrBathrooms__lte=filters.get('bathrooms_to')),
                Q(constructionYear__gte=filters.get('year_built_from')),
                Q(constructionYear__lte=filters.get('year_built_to')),
                Q(type__contains=filters.get('type'))
            ).order_by(request.GET.get('order'))]
        return JsonResponse({'data': properties})

    context = {'country_list': country_list,
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
    num_favorites = Favorites.objects.filter(property_id=prop_id).count()
    # If the user is loged in the property is added to his recently viewed
    if request.user.is_authenticated:
        recently_viewed = RecentlyViewed()
        recently_viewed.timestamp = datetime.now()
        recently_viewed.property = property
        recently_viewed.user = request.user
        recently_viewed.save()
        is_favorite = Favorites.objects.filter(property_id=property.id).filter(user_id=request.user).count() != 0
    context = {'property': property,
               'attributes': Attribute.objects.order_by('description'),
               'is_favorite': is_favorite,
               'num_favorites': num_favorites}
    return render(request, 'realEstate/property-details.html', context)


@login_required()
def favorite_property(request, prop_id):
    if request.is_ajax() and request.method == 'POST' and 'fav' in request.POST:
        property = get_object_or_404(Property, pk=prop_id)
        favorite = Favorites()
        favorite.property = property
        favorite.user = request.user
        favorite.save()
        return HttpResponse()
    else:
        return redirect('property-details', prop_id)


@login_required()
def unfavorite_property(request, prop_id):
    if request.is_ajax() and request.method == 'POST' and 'unfav' in request.POST:
        favorite = get_object_or_404(Favorites, property_id=prop_id, user_id=request.user)
        favorite.delete()
        return HttpResponse()
    else:
        return redirect('property-details', prop_id)


@login_required
def create_property(request):
    images_form_set = modelformset_factory(PropertyImage, fields=('image',), extra=5)
    if request.method == 'POST':
        address_form = AddressForm(data=request.POST)
        property_form = PropertyForm(data=request.POST)
        image_form = images_form_set(data=request.POST)

        if property_form.is_valid() and address_form.is_valid() and image_form.is_valid():
            # Saving to the database:
            prop = property_form.save(commit=False)
            prop.seller = User.objects.get(pk=request.user.id)
            address = address_form.save(commit=False)
            address.country = request.POST['country-list']
            address.save()
            prop.address = address
            prop.save()
            property_form.save_m2m()

            images = image_form.save(commit=False)
            for image in images:
                image.property_id = prop.id
                image.save()

            return redirect(reverse('user-profile'))
        else:
            # The user reenters invalid information.
            context = { 'address_form': address_form,
                        'property_form': property_form,
                        'image_form': image_form, }
            return render(request, 'realEstate/add-property.html', context)
    else:
        # The page is initially loaded with blank a form.
        context = { 'address_form': AddressForm(),
                    'property_form': PropertyForm(),
                    'image_form': images_form_set(queryset=PropertyImage.objects.none()), }
        return render(request, 'realEstate/add-property.html', context)


@login_required
def update_property(request, prop_id):
    property_instance = Property.objects.get(pk=prop_id)
    images_form_set = inlineformset_factory(Property, PropertyImage, fields=('image',))

    if request.user.id != property_instance.seller.id:  # Incorrect user
        return redirect(reverse('user-profile'))

    if request.method == 'POST':
        property_form = PropertyForm(data=request.POST, instance=property_instance)
        address_form = AddressForm(data=request.POST, instance=property_instance.address)
        image_form = images_form_set(data=request.POST, instance=property_instance)

        if property_form.is_valid() and address_form.is_valid() and image_form.is_valid():
            # Saving to the database:
            prop = property_form.save(commit=False)
            address = address_form.save(commit=False)
            address.country = request.POST['country-list']
            address.save()
            prop.address = address
            prop.save()
            property_form.save_m2m()

            image_form.save()
            return redirect(reverse('user-profile'))
        else:
            # The user reenters invalid information.
            context = { 'pk': prop_id,
                        'address_form': address_form,
                        'property_form': property_form,
                        'image_form': image_form, }
            return render(request, 'realEstate/edit-property.html', context)
    else:
        # The page is initially loaded with blank a form.
        context = {'pk': prop_id,
                   'address_form': AddressForm(instance=property_instance.address),
                   'property_form': PropertyForm(instance=property_instance),
                   'image_form': images_form_set(instance=property_instance), }
        return render(request, 'realEstate/edit-property.html', context)
