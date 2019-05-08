from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', views.index, name='property-index'),
    path('<int:id>', views.property_details, name='property-details'),
    path('', views.filter, name="filter")
]