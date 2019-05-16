from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', views.index, name='property-index'),
    path('<int:prop_id>', views.property_details, name='property-details'),
    path('add-property', views.create_property, name='add-property'),
    path('edit-property/<int:prop_id>', views.update_property, name='edit-property'),
    path('unfavorite-property/<int:prop_id>', views.unfavorite_property, name="unfavorite-property"),
    path('favorite-property/<int:prop_id>', views.favorite_property, name="favorite-property"),
]