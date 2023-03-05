from django.urls import include, path
from . import views
from .views import *
from rest_framework import routers



system_url = routers.SimpleRouter()
system_url.register(r'sensory_data',SensoryDataViewSet)
system_url.register(r'chart_config',ChartConfigViewSet)

urlpatterns = [

    path('sensory_data/get_average_temperatures/', average_temperatures),
    path('sensory_data/get_average_salinity/', average_salinity),
    path('sensory_data/get_average_ph/', average_ph),

    path('chart_config/get_demo_chart_json/', get_demo_chart_json),


]

urlpatterns+= system_url.urls

