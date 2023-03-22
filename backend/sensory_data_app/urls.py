from django.urls import include, path
from . import views
from .views import *
from rest_framework import routers


system_url = routers.SimpleRouter()
system_url.register(r'sensory_data', SensoryDataViewSet)
system_url.register(r'chart_config', ChartConfigViewSet)

urlpatterns = [

    path('sensory_data/get_average_temperatures/', average_temperatures),
    path('sensory_data/get_average_salinity/', average_salinity),
    path('sensory_data/get_average_ph/', average_ph),

    path('chart_config/get_demo_chart_json/', get_demo_chart_json),
    path('chart_config/get_demo_chart_json_two/', get_demo_chart_json_two),
    path('chart_config/get_demo_chart_json_three/', get_demo_chart_json_three),
    path('chart_config/get_demo_chart_json_four/', get_demo_chart_json_four),
    path('chart_config/get_demo_chart_json_five/', get_demo_chart_json_five),

    # for dynamic charts - single endpoint
    path('chart_config/get_charts_data/', get_charts_data),

]

urlpatterns += system_url.urls
