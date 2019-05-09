from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

# my profile etc.
urlpatterns = [
    path('', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('profile', views.profile, name='user-profile'),
    path('add-property/', views.add_property, name='add_property'),
    path('login', LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout', LogoutView.as_view(next_page='login'), name='logout'),
    path('register', views.register, name='register')
]