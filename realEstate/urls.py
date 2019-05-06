from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', views.index, name='index'),
    path('property', views.property, name='property'),
]