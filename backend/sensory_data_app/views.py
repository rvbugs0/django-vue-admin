from django.shortcuts import render

import json
from .models import SensoryData
from .models import ChartConfig
# Create your views here.

from rest_framework import serializers
from rest_framework.response import Response
from dvadmin.utils.json_response import DetailResponse, SuccessResponse
from dvadmin.utils.viewset import CustomModelViewSet
from django.http import HttpResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from dvadmin.utils.serializers import CustomModelSerializer


from rest_framework.decorators import action
from dvadmin.utils.permission import AnonymousUserPermission


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
@action(methods=["GET"], detail=False, permission_classes=[AnonymousUserPermission])
@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def average_temperatures(request):
    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    data = SensoryData.objects.values("sea_water_temperature_c")

    data = SensoryData.objects.all()
    if (len(data) == 0):
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
    if (len(data) == 0):
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
    if (len(data) == 0):
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


class ChartConfigSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """
    public_exposed = serializers.BooleanField(required=True)
    entity = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    title = serializers.CharField(required=True)
    function_type = serializers.CharField(required=True)

    class Meta:
        model = ChartConfig
        fields = "__all__"
        read_only_fields = ["id"]


class ChartConfigViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = ChartConfig.objects.all()
    serializer_class = ChartConfigSerializer




@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_charts_data(request):
    res = []
    chart_configs = ChartConfig.objects.filter(public_exposed=True)
    for c in chart_configs:
        if (c.function_type == "monthly_average"):
            data_objects = SensoryData.objects.all()
            data = get_average_monthly_within_range(data_objects, c.entity)
            if (c.type == "bar" or c.type == "area" or c.type == "line"):
                xData = []
                yData = []
                for monthly_data in data:
                    xData.append(monthly_data[0])
                    yData.append(monthly_data[1])
                res_object = {}
                res_object["id"] = c.id
                res_object["xData"] = xData
                res_object["yData"] = yData
                res_object["type"] = c.type
                res_object["title"] = c.title
                res.append(res_object)

        if (c.function_type == "monthly_max" or c.function_type == "monthly_min"):
            data_objects = SensoryData.objects.all()
            data = []
            if (c.function_type == "monthly_max"):
                data = get_max_of_month(data_objects, c.entity)
            else:
                data = get_min_of_month(data_objects, c.entity)
            if (c.type == "bar" or c.type == "area" or c.type == "line"):
                xData = []
                yData = []
                for monthly_data in data:
                    xData.append(monthly_data[0])
                    yData.append(monthly_data[1])
                res_object = {}
                res_object["id"] = c.id
                res_object["xData"] = xData
                res_object["yData"] = yData
                res_object["type"] = c.type
                res_object["title"] = c.title
                res.append(res_object)

    return HttpResponse(json.dumps(res), content_type="application/json")


def get_average_monthly_within_range(data, entity):
    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    # data = SensoryData.objects.all()
    if (len(data) == 0):
        return [(m, 0) for m in months]

    monthlyData = [[0] for i in range(12)]
    for i in data:
        dt = int(str(i.date_recorded).split("-")[1])
        if (entity == "sea_water_temperature_c"):
            monthlyData[dt-1].append(i.sea_water_temperature_c)
        elif (entity == "salinity"):
            monthlyData[dt-1].append(i.salinity)
        elif (entity == "ph"):
            monthlyData[dt-1].append(i.ph)
        elif (entity == "dissolved_oxygen"):
            monthlyData[dt-1].append(i.dissolved_oxygen)

    res = []
    for i in range(len(monthlyData)):
        res.append(
            (months[i], str(sum(monthlyData[i]) / max(0.000000001, (len(monthlyData[i])-1)))))
    return res


def get_max_of_month(data, entity):
    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    if (len(data) == 0):
        return [(m, 0) for m in months]

    monthlyData = [[0] for i in range(12)]
    for i in data:
        dt = int(str(i.date_recorded).split("-")[1])
        if (entity == "sea_water_temperature_c"):
            monthlyData[dt-1].append(i.sea_water_temperature_c)
        elif (entity == "salinity"):
            monthlyData[dt-1].append(i.salinity)
        elif (entity == "ph"):
            monthlyData[dt-1].append(i.ph)
        elif (entity == "dissolved_oxygen"):
            monthlyData[dt-1].append(i.dissolved_oxygen)

    res = []
    for i in range(len(monthlyData)):
        res.append(
            (months[i], str(max(monthlyData[i]))))
    return res


def get_min_of_month(data, entity):
    months = ['Jan', 'Feb', 'March', 'April', 'May',
              'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    if (len(data) == 0):
        return [(m, 0) for m in months]

    monthlyData = [[0] for i in range(12)]
    for i in data:
        dt = int(str(i.date_recorded).split("-")[1])
        if (entity == "sea_water_temperature_c"):
            monthlyData[dt-1].append(i.sea_water_temperature_c)
        elif (entity == "salinity"):
            monthlyData[dt-1].append(i.salinity)
        elif (entity == "ph"):
            monthlyData[dt-1].append(i.ph)
        elif (entity == "dissolved_oxygen"):
            monthlyData[dt-1].append(i.dissolved_oxygen)

    res = []
    for i in range(len(monthlyData)):
        if (len(monthlyData[i]) <= 1):
            continue
        monthlyData[i].pop(0)
        res.append(
            (months[i], str(min(monthlyData[i]))))
    return res
