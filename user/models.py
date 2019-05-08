from django.db import models
from realEstate.models import Property, Address
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=255),
    email = models.CharField(max_length=255),
    phone = models.CharField(max_length=32),
    password = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.name


class RecentlyViewed(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


class Favorites(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ActiveListings(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PaymentInfo(models.Model):
    cardNumber = models.CharField(max_length=16)
    cardName = models.CharField(max_length=255)
    cardCVC = models.IntegerField()
    cardExpiryMonth = models.IntegerField()
    cardExpiryYear = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    def __str__(self):
        return self.cardNumber


class Purchase(models.Model):
    SSN = models.CharField(max_length=32)
    userInfo = models.ForeignKey(User,on_delete=models.CASCADE)
    paymentInfo = models.ForeignKey(PaymentInfo, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)