from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', views.index, name='user-index'),
    path('profile', views.profile, name='user-profile'),
]