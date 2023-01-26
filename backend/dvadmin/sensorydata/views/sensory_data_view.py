from rest_framework import serializers
from rest_framework.response import Response
from dvadmin.utils.json_response import DetailResponse, SuccessResponse


from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.system.models import SensoryData
from django.http import HttpResponse

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from dvadmin.utils.serializers import CustomModelSerializer


class SensoryDataSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """
    sea_water_temperature_c = serializers.FloatField(required=True)
    salinity = serializers.FloatField(required=True)
    ph = serializers.FloatField(required=True)
    dissolved_oxygen = serializers.FloatField(required=True)
    date_recorded = serializers.DateTimeField(required=True)

    class Meta:
        model = SensoryData
        fields = "__all__"
        read_only_fields = ["id"]



class SensoryDataViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = SensoryData.objects.all()
    serializer_class = SensoryDataSerializer


# view set has all the basic apis and custom api's are addded below and their urls also added in the urls.py

