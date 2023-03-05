from django.db import models
from dvadmin.utils.models import CoreModel


# Create your models here.

class SensoryData(CoreModel):
    sea_water_temperature_c = models.FloatField()
    salinity = models.FloatField()
    ph = models.FloatField()
    dissolved_oxygen = models.FloatField()
    date_recorded = models.DateTimeField()


class ChartConfig(CoreModel):
    data_api = models.CharField(default="index",blank=False,max_length=200)
    public_exposed = models.BooleanField(default=True)
    chart_name = models.CharField(default="New Chart",blank=False,max_length=100)


