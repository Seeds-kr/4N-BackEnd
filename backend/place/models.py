from django.db import models

# Create your models here.
class Places(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
         return f"Name: {self.name}, Address: {self.address}, Phone: {self.phone}, Latitude: {self.latitude}, Longitude: {self.longitude}"