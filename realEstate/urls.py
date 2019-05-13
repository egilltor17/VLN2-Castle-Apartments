from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', views.index, name='property-index'),
    path('<int:prop_id>', views.property_details, name='property-details'),
    path('add-property', views.create, name='add_property'),
    path('edit-property/<int:prop_id>', views.update, name='edit_property'),
]