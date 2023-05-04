from django.db import models
from dvadmin.utils.models import CoreModel
from django.utils import timezone

# Create your models here.

class SensoryData(CoreModel):
    sea_water_temperature_c = models.FloatField()
    salinity = models.FloatField()
    ph = models.FloatField()
    dissolved_oxygen = models.FloatField()
    date_recorded = models.DateTimeField()



class ChartConfig(CoreModel):
    entity = models.CharField(default="sea_water_temperature_c", blank=False, max_length=50)
    function_type = models.CharField(default="monthly_average", blank=False, max_length=50)
    type = models.CharField(default="bar", blank=False, max_length=20)
    public_exposed = models.BooleanField(default=True)
    title = models.CharField(default="Avg monthly sea water temp. deg Celcius", blank=False, max_length=100)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)


class SensoryDataRangeAlert(CoreModel):
    entity = models.CharField(default="sea_water_temperature_c", blank=False, max_length=50)
    upper_treshold = models.FloatField(default=100,blank=False)
    lower_treshold = models.FloatField(default=-100,blank=False)
