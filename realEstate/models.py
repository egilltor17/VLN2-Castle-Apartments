from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Address(models.Model):
    country = models.CharField(max_length=255)
    municipality = models.CharField(max_length=255, blank=True, null=True)  # State, provance, region.
    city = models.CharField(max_length=255)
    postCode = models.CharField(max_length=16)
    streetName = models.CharField(max_length=255)
    houseNumber = models.CharField(max_length=16)
    apartmentNumber = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return ', '.join([self.streetName + ' ' + self.houseNumber,
                          ('apartment ' + self.apartmentNumber + ', ' if self.apartmentNumber else '') + self.postCode,
                          self.city,
                          (self.municipality + ', ' if self.municipality else '') + self.country])


class Attribute(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Property(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2048, blank=True)
    type = models.CharField(max_length=255)
    price = models.FloatField()
    nrBedrooms = models.IntegerField()
    nrBathrooms = models.IntegerField()
    squareMeters = models.IntegerField()
    constructionYear = models.IntegerField()
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    attributes = models.ManyToManyField(Attribute)
    dateCreated = models.DateTimeField(default=timezone.now)
    sold = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    image = models.CharField(max_length=1024)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
