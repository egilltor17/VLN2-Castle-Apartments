from django.contrib.auth.models import User
from django.db import models
from realEstate.models import Property, Address
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32, blank=True, null=True)
    # A better way to store images
    profileImage = models.ImageField(upload_to='profileImages/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class RecentlyViewed(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()


class Favorites(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class PaymentInfo(models.Model):
    cardNumber = models.CharField(max_length=16)
    cardName = models.CharField(max_length=255)
    cardCVC = models.IntegerField()
    cardExpiryMonth = models.IntegerField()
    cardExpiryYear = models.IntegerField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        return '**** **** **** ' + self.cardNumber[-4:]


class Purchase(models.Model):
    SSN = models.CharField(max_length=32)
    userInfo = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentInfo = models.OneToOneField(PaymentInfo, on_delete=models.CASCADE)
    property = models.OneToOneField(Property, on_delete=models.CASCADE)

    def __str__(self):
        return self.id
