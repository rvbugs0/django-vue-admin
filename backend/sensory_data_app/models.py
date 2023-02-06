from django.db import models
from dvadmin.utils.models import CoreModel


# Create your models here.

class SensoryData(CoreModel):
    sea_water_temperature_c = models.FloatField()
    salinity = models.FloatField()
    ph = models.FloatField()
    dissolved_oxygen = models.FloatField()
    date_recorded = models.DateTimeField()
