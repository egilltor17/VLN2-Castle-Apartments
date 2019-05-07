from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about_us, name='about-us'),
]