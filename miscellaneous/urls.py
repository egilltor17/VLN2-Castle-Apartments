from django.urls import path

from . import views

# my profile etc.
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about_us, name='about-us'),
    path('purchase/<int:prop_id>', views.purchase, name='purchase'),
    path('purchase/receipt/<int:pur_id>', views.purchase_receipt, name='purchase-receipt'),
]