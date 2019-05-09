from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', views.index, name='user-index'),
    path('profile', views.profile, name='user-profile'),
    #path('list_property', views.list_property, name='list_property'),
    path('add-property/', views.add_property, name='add_property')
]