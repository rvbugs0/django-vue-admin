from django.db.models import F
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

from django.db.models import Avg
from django.db.models.functions import TruncMonth
from django.db.models import Max
from django.db.models import Min


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

class ExportSensoryDataSerializer(CustomModelSerializer):
    
    sea_water_temperature_c = serializers.FloatField( default=0.0)
    salinity = serializers.FloatField( default=0.0)
    dissolved_oxygen = serializers.FloatField( default = 0.0)
    ph = serializers.FloatField( default = 0.0)
    date_recorded = serializers.DateTimeField( default = "")
    class Meta:
        model = SensoryData
        fields = (
            "sea_water_temperature_c",
            "salinity",
            "dissolved_oxygen",
            "ph",
            "date_recorded"
        )




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

    export_field_label = {
            "sea_water_temperature_c":"Sea water temperature in Degree Celcius",
            "salinity":"Salinity",
            "dissolved_oxygen":"Dissolved Oxygen",
            "ph":"pH",
            "date_recorded":"Date recorded"

    }
    export_serializer_class = ExportSensoryDataSerializer


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
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)

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
        if (c.function_type == "plain_value"):
            data = get_plain_data_within_range( c.start_date, c.end_date, c.entity)

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

        if (c.function_type == "monthly_average"):

            data = get_average_monthly_within_range(
                c.start_date, c.end_date, c.entity)

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

            data = []
            if (c.function_type == "monthly_max"):
                data = get_max_of_month(c.start_date, c.end_date, c.entity)
            else:
                data = get_min_of_month(c.start_date, c.end_date, c.entity)
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


# articles = Article.objects.values('title').annotate(article_title=F('title'))


def get_average_monthly_within_range(start_date, end_date, entity):

    average_val_by_month = SensoryData.objects.filter(
        date_recorded__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('date_recorded')
    ).values(
        'month'
    ).annotate(
        avg_val=Avg(entity)
    ).order_by('month')
    res = []
    for data in average_val_by_month:
        res.append((data['month'].strftime('%B %Y'), data['avg_val']))
        # print(f"Month: {} Average Temperature: {]}")

    return res


def get_plain_data_within_range(start_date, end_date, entity):

    records = SensoryData.objects.filter(
        date_recorded__range=(start_date, end_date)
    ).annotate(
        entity_value=F(entity)
    ).values(
        'entity_value','date_recorded'
    )
    res = []
    
    for data in records:
        obj = data["date_recorded"]
        day = obj.strftime('%d')
        month = obj.strftime('%m')
        year = obj.strftime('%Y')
        d = year + "-" + month + "-" + day
        res.append((d, data['entity_value']))


    return res




def get_max_of_month(start_date, end_date, entity):
    max_val_by_month = SensoryData.objects.filter(
        date_recorded__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('date_recorded')
    ).values(
        'month'
    ).annotate(
        max_val=Max(entity)
    ).order_by('month')
    res = []
    for data in max_val_by_month:
        res.append((data['month'].strftime('%B %Y'), data['max_val']))
    return res


def get_min_of_month(start_date, end_date, entity):
    min_val_by_month = SensoryData.objects.filter(
        date_recorded__range=(start_date, end_date)
    ).annotate(
        month=TruncMonth('date_recorded')
    ).values(
        'month'
    ).annotate(
        min_val=Min(entity)
    ).order_by('month')
    res = []
    for data in min_val_by_month:
        res.append((data['month'].strftime('%B %Y'), data['min_val']))

    return res
