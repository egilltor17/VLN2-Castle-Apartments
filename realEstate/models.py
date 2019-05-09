from django.contrib.auth.models import User
from django.db import models
# from user.models import Profile
# Create your models here.


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
                          ('apartment ' + self.apartmentNumber if self.apartmentNumber else ' '),
                          self.postCode,
                          self.city,
                          (self.municipality if self.municipality else ' '),
                          self.country])


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
    dateCreated = models.DateTimeField()
    sold = models.BooleanField()

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    image = models.CharField(max_length=1024)
    # TODO: change property images
    # image = models.ImageField(upload_to='propertyImages/', blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)


class PropertyAttribute(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)