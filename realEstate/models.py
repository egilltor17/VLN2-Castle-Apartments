from django.db import models
# from user.models import User
# Create your models here.


class Address(models.Model):
    country = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255, blank=True)  # State, province, region.
    city = models.CharField(max_length=255)
    postCode = models.CharField(max_length=16)
    streetName = models.CharField(max_length=255)
    houseNumber = models.CharField(max_length=16)
    apartmentNumber = models.CharField(max_length=16, blank=True)


class Attribute(models.Model):
    description = models.CharField(max_length=255)


class Property(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(max_length=255)
    price = models.FloatField()
    nrBedrooms = models.IntegerField()
    nrBathrooms = models.IntegerField()
    squareMeters = models.IntegerField()
    constructionYear = models.IntegerField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    # seller = models.ForeignKey(User, on_delete=models.CASCADE)
    sellerName = models.CharField(max_length=255)
    sellerEmail = models.CharField(max_length=255)
    sellerPhone = models.CharField(max_length=32)
    dateCreated = models.DateTimeField()
    sold = models.BooleanField
    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    image = models.CharField(max_length=1024)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)


class PropertyAttribute(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)