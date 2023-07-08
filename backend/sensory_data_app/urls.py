from django.urls import include, path
from . import views
from .views import *
from rest_framework import routers


system_url = routers.SimpleRouter()
system_url.register(r'air_sensor_data', AIRSensorDataViewSet)
system_url.register(r'th_sensor_data', THSensorDataViewSet)
system_url.register(r'chart_config', ChartConfigViewSet)
system_url.register(r'sensory_alerts', SensoryDataRangeAlertViewSet)
system_url.register(r'violation_alerts_list', ViolationAlertsListViewSet)


urlpatterns = [

    # path('sensory_data/get_data_within_range/', get_data_within_range),
    # path('sensory_data/export_data_to_excel/', export_data_to_excel),


    # for dynamic charts - single endpoint
    path('chart_config/get_charts_data/', get_charts_data),
    # path('chart_config/get_plain_scroll_charts/', get_plain_line_chart_data),
    path('sensory_alerts/get_th_sensor_violation_data',get_th_sensor_violation_data),
    path('sensory_alerts/get_air_sensor_violation_data',get_air_sensor_violation_data),
    # path('sensory_alerts/send_email_alerts',send_email_alerts)



    
]

urlpatterns += system_url.urls
