from django.db import models

# Create your models here.

class FuelStation(models.Model):
    truckstop_id= models.CharField(unique=True,max_length=300)
    truckstop_name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    state = models.CharField(max_length=50)
    rack_id = models.IntegerField()
    retail_price = models.DecimalField(max_digits=5, decimal_places=3)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.truckstop_name}, {self.retail_price}"
