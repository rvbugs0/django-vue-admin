from django.urls import include, path
from . import views
from .views import *
from rest_framework import routers


system_url = routers.SimpleRouter()
system_url.register(r'sensory_data', SensoryDataViewSet)
system_url.register(r'chart_config', ChartConfigViewSet)
system_url.register(r'sensory_alerts', SensoryDataRangeAlertViewSet)

urlpatterns = [

    path('sensory_data/get_average_temperatures/', average_temperatures),
    path('sensory_data/get_average_salinity/', average_salinity),
    path('sensory_data/get_average_ph/', average_ph),
    path('sensory_data/get_data_within_range/', get_data_within_range),
    path('sensory_data/export_data_to_excel/', export_data_to_excel),


    # for dynamic charts - single endpoint
    path('chart_config/get_charts_data/', get_charts_data),
    path('chart_config/get_plain_scroll_charts/', get_plain_line_chart_data),
    path('sensory_alerts/get_sensory_violation_data',get_sensory_violation_data)
]

urlpatterns += system_url.urls
