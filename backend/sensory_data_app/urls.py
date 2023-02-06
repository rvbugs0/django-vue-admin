from django.urls import include, path
from . import views
from .views import *
from rest_framework import routers



system_url = routers.SimpleRouter()
system_url.register(r'sensory_data',SensoryDataViewSet)

urlpatterns = [

    path('sensory_data/get_average_temperatures/', average_temperatures),
    path('sensory_data/get_average_salinity/', average_salinity),
    path('sensory_data/get_average_ph/', average_ph),


]

urlpatterns+= system_url.urls

