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
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def average_temperatures(request):
    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    data = SensoryData.objects.all()
    if(len(data)==0):
        return HttpResponse("{}", content_type="application/json")



    monthlyData = [[0] for i in range(12)]
    for i in data:
        dt = int(str(i.date_recorded).split("-")[1])
        monthlyData[dt-1].append(i.sea_water_temperature_c)

    res = "["
    for i in range(len(monthlyData)-1):
        if (len(monthlyData[i])-1 > 0):
            res += "{\"month\":\""
            res += months[i]
            res += "\",\"average_temp\":"
            res += str(sum(monthlyData[i]) / (len(monthlyData[i])-1))
            res += "},"
    if (len(monthlyData[11]) > 1):
        res += "{\"month\":\""
        res += months[11]
        res += "\",\"average_temp\":"
        res += str(sum(monthlyData[11]) / (len(monthlyData[11])-1))
        res += "}"
    else:
        res = res[:len(res)-1]

    res += "]"
    return HttpResponse(res, content_type="application/json")

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def average_salinity(request):
    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    data = SensoryData.objects.all()
    if(len(data)==0):
        return HttpResponse("{}", content_type="application/json")



    monthlyData = [[0] for i in range(12)]
    for i in data:
        dt = int(str(i.date_recorded).split("-")[1])
        monthlyData[dt-1].append(i.salinity)

    res = "["
    for i in range(len(monthlyData)-1):
        if (len(monthlyData[i])-1 > 0):
            res += "{\"month\":\""
            res += months[i]
            res += "\",\"average_salinity\":"
            res += str(sum(monthlyData[i]) / (len(monthlyData[i])-1))
            res += "},"
    if (len(monthlyData[11]) > 1):
        res += "{\"month\":\""
        res += months[11]
        res += "\",\"average_salinity\":"
        res += str(sum(monthlyData[11]) / (len(monthlyData[11])-1))
        res += "}"
    else:
        res = res[:len(res)-1]

    res += "]"
    return HttpResponse(res, content_type="application/json")

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def average_ph(request):
    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    data = SensoryData.objects.all()
    if(len(data)==0):
        return HttpResponse("{}", content_type="application/json")



    monthlyData = [[0] for i in range(12)]
    for i in data:
        dt = int(str(i.date_recorded).split("-")[1])
        monthlyData[dt-1].append(i.salinity)

    res = "["
    for i in range(len(monthlyData)-1):
        if (len(monthlyData[i])-1 > 0):
            res += "{\"month\":\""
            res += months[i]
            res += "\",\"average_ph\":"
            res += str(sum(monthlyData[i]) / (len(monthlyData[i])-1))
            res += "},"
    if (len(monthlyData[11]) > 1):
        res += "{\"month\":\""
        res += months[11]
        res += "\",\"average_ph\":"
        res += str(sum(monthlyData[11]) / (len(monthlyData[11])-1))
        res += "}"
    else:
        res = res[:len(res)-1]

    res += "]"
    return HttpResponse(res, content_type="application/json")

