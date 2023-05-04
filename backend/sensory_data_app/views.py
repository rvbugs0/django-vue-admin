from openpyxl import Workbook
from django.http import JsonResponse
from datetime import datetime
from django.db.models import F
from django.shortcuts import render

import json
from .models import SensoryData
from .models import ChartConfig
from .models import SensoryDataRangeAlert
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

    sea_water_temperature_c = serializers.FloatField(default=0.0)
    salinity = serializers.FloatField(default=0.0)
    dissolved_oxygen = serializers.FloatField(default=0.0)
    ph = serializers.FloatField(default=0.0)
    date_recorded = serializers.DateTimeField(default="")

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
        "sea_water_temperature_c": "Sea water temperature in Degree Celcius",
        "salinity": "Salinity",
        "dissolved_oxygen": "Dissolved Oxygen",
        "ph": "pH",
        "date_recorded": "Date recorded"

    }
    export_serializer_class = ExportSensoryDataSerializer


# --------------------------- alerts ---------------


class SensoryDataRangeAlertSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """
    entity = serializers.CharField(required=True)
    upper_treshold = serializers.FloatField(required=True)
    lower_treshold = serializers.FloatField(required=True)

    class Meta:
        model = SensoryDataRangeAlert
        fields = "__all__"
        read_only_fields = ["id"]


class SensoryDataRangeAlertViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = SensoryDataRangeAlert.objects.all()
    serializer_class = SensoryDataRangeAlertSerializer


# -------------- end - alerts ----------------------------


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
            data = get_plain_data_within_range(
                c.start_date, c.end_date, c.entity)

            if (c.type == "bar" or c.type == "area" or c.type == "line" or c.type == "scroll_chart"):
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
        'entity_value', 'date_recorded'
    ).order_by('date_recorded')
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


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_data_within_range(request):

    start_date = request.GET.get('start_date')

    end_date = request.GET.get('end_date')
    page = int(request.GET.get('page', 1))
    limit = int(request.GET.get('limit', 10))

    # Parse the datetime string
    dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    e_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    # Extract the date part and format it as a string
    date_str = dt.strftime("%Y-%m-%d")
    end_date_str = e_dt.strftime("%Y-%m-%d")
    start_date = date_str
    end_date = end_date_str
    # print("Start date ", start_date)

    data_queryset = SensoryData.objects.filter(
        date_recorded__range=(start_date, end_date)

        #  date_recorded__date=start_date
    )

    # print("hello")
    res = []

    for d in data_queryset:
        data = {"sea_water_temperature_c": d.sea_water_temperature_c, "salinity": d.salinity,
                "dissolved_oxygen": d.dissolved_oxygen, "ph": d.ph, "date_recorded": d.date_recorded.strftime('%Y-%m-%d %H:%M:%S')}
        res.append(data)

    # total = data_queryset.count()

    # if page < 1:
    #     page = 1

    # start_index = (page - 1) * limit
    # end_index = start_index + limit
    # data = [start_index:end_index].values()

    # print(data)

    response = {
        "code": 2000,
        "msg": "success",
        "data": {
            "page": page,
            "total": len(res),
            "limit": len(res),
            "data": res,
        }
    }

    return HttpResponse(json.dumps(response), content_type="application/json")


def export_data_to_excel(request):

    start_date = request.GET.get('date_recorded')

    # Parse the datetime string
    dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Extract the date part and format it as a string
    date_str = dt.strftime("%Y-%m-%d")
    start_date = date_str

    end_date = request.GET.get('end_date')
    e_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    end_date_str = e_dt.strftime("%Y-%m-%d")
    end_date = end_date_str

    data = SensoryData.objects.filter(
        date_recorded__range=(start_date, end_date)

        #  date_recorded__date=start_date
    )

    # Create a new workbook
    wb = Workbook()

    # Select the active worksheet
    ws = wb.active

    # Write the column headers to the worksheet
    ws.append(['Sea Water Temperature in Degree Celcius',
              'Salinity', 'Dissolved Oxygen', 'pH', "Date Recorded"])

    # Write the data to the worksheet
    for row in data:
        ws.append([row.sea_water_temperature_c, row.salinity, row.dissolved_oxygen,
                  row.ph, row.date_recorded.strftime('%Y-%m-%d %H:%M:%S')])

    # Create a response object with the appropriate content type
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Set the content-disposition header to force a download
    response['Content-Disposition'] = 'attachment; filename=export.xlsx'

    # Write the workbook data to the response
    wb.save(response)

    # Return the response
    return response


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_plain_line_chart_data(request):
    res = []
    entity = request.GET.get('entity')
    data = SensoryData.objects.all().order_by(
        'date_recorded').values('date_recorded', entity)
    xData = []
    yData = []
    for record in data:

        obj = record["date_recorded"]
        day = obj.strftime('%d')
        month = obj.strftime('%m')
        year = obj.strftime('%Y')
        d = year + "-" + month + "-" + day
        xData.append(d)
        yData.append(record[entity])
    res_object = {}
    res_object["xData"] = xData
    res_object["yData"] = yData
    res_object["title"] = entity
    res.append(res_object)

    return HttpResponse(json.dumps(res), content_type="application/json")


from django.db.models import Q

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_sensory_violation_data(request):
    
    range_filters = SensoryDataRangeAlert.objects.all()
    if (len(range_filters) == 0):
        return HttpResponse(json.dumps([]), content_type="application/json")

    tresholds = {}
    tresholds["sea_water_temperature_c"] = [-9999, 99999]
    tresholds["salinity"] = [-9999999, 9999999]
    tresholds["ph"] = [-99999, 9999999]
    tresholds["dissolved_oxygen"] = [-9999999, 9999999]

    for i in range_filters:
        tresholds[i.entity] = [i.lower_treshold, i.upper_treshold]

    data = SensoryData.objects.filter(
        Q(sea_water_temperature_c__lt = tresholds["sea_water_temperature_c"][0]) |
        Q(sea_water_temperature_c__gt = tresholds["sea_water_temperature_c"][1]) | 
        Q(salinity__lt=tresholds["salinity"][0]) | 
        Q(salinity__gt=tresholds["salinity"][1]) |
        Q(ph__lt=tresholds["ph"][0]) | 
        Q(ph__gt=tresholds["ph"][1]) |
        Q(dissolved_oxygen__lt=tresholds["dissolved_oxygen"][0]) | 
        Q(dissolved_oxygen__gt=tresholds["dissolved_oxygen"][1])).order_by('date_recorded').values('date_recorded','salinity','ph','dissolved_oxygen','sea_water_temperature_c',"id")
    
    res = []
    for record in data:

        obj = record["date_recorded"]
        day = obj.strftime('%d')
        month = obj.strftime('%m')
        year = obj.strftime('%Y')
        d = year + "-" + month + "-" + day
        obj = {}
        obj["id"]= record["id"]
        obj["date_recorded"] = d
        obj["sea_water_temperature_c"] = record["sea_water_temperature_c"]
        obj["salinity"] = record["salinity"]
        obj["ph"] = record["ph"]
        obj["dissolved_oxygen"] = record["dissolved_oxygen"]
        # print(obj)
        res.append(obj)
    
    r = {}
    r["data"]={"total":len(res),"page":1,"limit":len(res),"data":res}
    return HttpResponse(json.dumps(r), content_type="application/json")

