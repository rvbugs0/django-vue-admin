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

    entity = models.CharField(
        default="sea_water_temperature_c", blank=False, max_length=50)

    function_type = models.CharField(
        default="monthly_average", blank=False, max_length=50)

    type = models.CharField(
        default="bar", blank=False, max_length=20)
    public_exposed = models.BooleanField(default=True)
    title = models.CharField(
        default="Avg monthly sea water temp. deg Celcius", blank=False, max_length=100)
