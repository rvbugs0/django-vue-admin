from django.db.models import Q
from openpyxl import Workbook
from django.http import JsonResponse
from datetime import datetime
from django.db.models import F
from django.shortcuts import render

import json
from .models import AIRSensorData
from .models import THSensorData
from .models import ChartConfig
from .models import SensoryDataRangeAlert
from .models import ViolationAlertsList

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


from django.core.mail import send_mail
from tabulate import tabulate


class AIRSensorDataSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """
    SO2_value = serializers.FloatField(required=True)
    NO2_value = serializers.FloatField(required=True)
    O3_value = serializers.FloatField(required=True)
    sensor_location = serializers.CharField()
    date_recorded = serializers.DateTimeField(required=True)

    class Meta:
        model = AIRSensorData
        fields = "__all__"
        read_only_fields = ["id"]


class ExportAIRSensorDataSerializer(CustomModelSerializer):

    SO2_value = serializers.FloatField(default=0.0)
    NO2_value = serializers.FloatField(default=0.0)
    O3_value = serializers.FloatField(default=0.0)
    sensor_location = serializers.CharField(default="")
    date_recorded = serializers.DateTimeField(default="")

    class Meta:
        model = AIRSensorData
        fields = (
            "SO2_value",
            "NO2_value",
            "O3_value",
            "sensor_location",
            "date_recorded"
        )


class AIRSensorDataViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = AIRSensorData.objects.all()
    serializer_class = AIRSensorDataSerializer

    export_field_label = {
        "SO2_value": "SO2 Value",
        "NO2_value": "NO2 Value",
        "O3_value": "O3 Value",
        "sensor_location": "Sensor Location",
        "date_recorded": "Date recorded"

    }
    export_serializer_class = ExportAIRSensorDataSerializer




class THSensorDataSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """
    humidity_value = serializers.FloatField(required=True)
    temperature_value = serializers.FloatField(required=True)
    sensor_location = serializers.CharField()
    date_recorded = serializers.DateTimeField(required=True)

    class Meta:
        model = THSensorData
        fields = "__all__"
        read_only_fields = ["id"]


class ExportTHSensorDataSerializer(CustomModelSerializer):

    humidity_value = serializers.FloatField(default=0.0)
    temperature_value = serializers.FloatField(default=0.0)
    sensor_location = serializers.CharField(default="")
    date_recorded = serializers.DateTimeField(default="")

    class Meta:
        model = THSensorData
        fields = (
            "humidity_value",
            "temperature_value",
            "sensor_location",
            "date_recorded"
        )


class THSensorDataViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = THSensorData.objects.all()
    serializer_class = THSensorDataSerializer

    export_field_label = {
        "temperature_value": "Temperature Value",
        "humidity_value": "Humidity Value",
        "sensor_location": "Sensor Location",
        "date_recorded": "Date recorded"

    }
    export_serializer_class = ExportTHSensorDataSerializer


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


# -------------- alerts-list ----------------------------

class ViolationAlertsListSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """
    email = serializers.CharField(required=True)

    class Meta:
        model = ViolationAlertsList
        fields = "__all__"
        read_only_fields = ["id"]


class ViolationAlertsListViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = ViolationAlertsList.objects.all()
    serializer_class = ViolationAlertsListSerializer


# view set has all the basic apis and custom api's are addded below and their urls also added in the urls.py

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

    table = None
    if entity in ["SO2_value","NO2_value","O3_value"]:
        table = AIRSensorData
    else:
        table = THSensorData
    average_val_by_month = table.objects.filter(
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
    table = None
    if entity in ["SO2_value","NO2_value","O3_value"]:
        table = AIRSensorData
    else:
        table = THSensorData

    records = table.objects.filter(
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
    table = None
    if entity in ["SO2_value","NO2_value","O3_value"]:
        table = AIRSensorData
    else:
        table = THSensorData

    max_val_by_month = table.objects.filter(
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
    table = None
    if entity in ["SO2_value","NO2_value","O3_value"]:
        table = AIRSensorData
    else:
        table = THSensorData

    min_val_by_month = table.objects.filter(
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
def get_th_data_within_range(request):

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

    data_queryset = THSensorData.objects.filter(
        date_recorded__range=(start_date, end_date)

        #  date_recorded__date=start_date
    )

    # print("hello")
    res = []

    for d in data_queryset:
        data = {"NO2_value": d.NO2_value, "SO2_value": d.SO2_value,
                "O3_value": d.O3_value, "sensor_location": d.sensor_location, "date_recorded": d.date_recorded.strftime('%Y-%m-%d %H:%M:%S')}
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


# def export_data_to_excel(request):
#     start_date = request.GET.get('date_recorded')

#     # Parse the datetime string
#     dt = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S.%fZ")

#     # Extract the date part and format it as a string
#     date_str = dt.strftime("%Y-%m-%d")
#     start_date = date_str

#     end_date = request.GET.get('end_date')
#     e_dt = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S.%fZ")
#     end_date_str = e_dt.strftime("%Y-%m-%d")
#     end_date = end_date_str

#     data = SensoryData.objects.filter(
#         date_recorded__range=(start_date, end_date)

#         #  date_recorded__date=start_date
#     )

#     # Create a new workbook
#     wb = Workbook()

#     # Select the active worksheet
#     ws = wb.active

#     # Write the column headers to the worksheet
#     ws.append(['Sea Water Temperature in Degree Celcius',
#               'Salinity', 'Dissolved Oxygen', 'pH', "Date Recorded"])

#     # Write the data to the worksheet
#     for row in data:
#         ws.append([row.sea_water_temperature_c, row.salinity, row.dissolved_oxygen,
#                   row.ph, row.date_recorded.strftime('%Y-%m-%d %H:%M:%S')])

#     # Create a response object with the appropriate content type
#     response = HttpResponse(
#         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

#     # Set the content-disposition header to force a download
#     response['Content-Disposition'] = 'attachment; filename=export.xlsx'

#     # Write the workbook data to the response
#     wb.save(response)

#     # Return the response
#     return response


# @api_view(('GET',))
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def get_plain_line_chart_data(request):
#     res = []
#     entity = request.GET.get('entity')
#     data = SensoryData.objects.all().order_by(
#         'date_recorded').values('date_recorded', entity)
#     xData = []
#     yData = []
#     for record in data:

#         obj = record["date_recorded"]
#         day = obj.strftime('%d')
#         month = obj.strftime('%m')
#         year = obj.strftime('%Y')
#         d = year + "-" + month + "-" + day
#         xData.append(d)
#         yData.append(record[entity])
#     res_object = {}
#     res_object["xData"] = xData
#     res_object["yData"] = yData
#     res_object["title"] = entity
#     res.append(res_object)

#     return HttpResponse(json.dumps(res), content_type="application/json")


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_th_sensor_violation_data(request):

    range_filters = SensoryDataRangeAlert.objects.all()
    if (len(range_filters) == 0):
        return HttpResponse(json.dumps([]), content_type="application/json")

    tresholds = {}
    # tresholds["SO2_value"] = [-9999, 99999]
    # tresholds["NO2_value"] = [-9999999, 9999999]
    # tresholds["O3_value"] = [-99999, 9999999]
    tresholds["temperature_value"] = [-9999999, 9999999]
    tresholds["humidity_value"] = [-9999999, 9999999]

    for i in range_filters:
        print(i.entity)
        tresholds[i.entity] = [i.lower_treshold, i.upper_treshold]


    data = THSensorData.objects.filter(
        Q(temperature_value__lt=tresholds["temperature_value"][0]) |
        Q(temperature_value__gt=tresholds["temperature_value"][1]) |
        Q(humidity_value__lt=tresholds["humidity_value"][0]) |
        Q(humidity_value__gt=tresholds["humidity_value"][1])).order_by('date_recorded').values('date_recorded', 'temperature_value', 'humidity_value','sensor_location', "id")

    res = []
    for record in data:

        obj = {}
        obj["id"] = record["id"]
        obj["sensor_location"] = record["sensor_location"]
        obj["date_recorded"] = record["date_recorded"].strftime("%Y-%m-%dT%H:%M:%S")
        obj["temperature_value"] = record["temperature_value"]
        obj["humidity_value"] = record["humidity_value"]
        # print(obj)
        res.append(obj)

    r = {}
    r["data"] = {"total": len(res), "page": 1, "limit": len(res), "data": res}
    return HttpResponse(json.dumps(r), content_type="application/json")


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_air_sensor_violation_data(request):

    range_filters = SensoryDataRangeAlert.objects.all()
    if (len(range_filters) == 0):
        return HttpResponse(json.dumps([]), content_type="application/json")

    tresholds = {}
    tresholds["SO2_value"] = [-9999, 99999]
    tresholds["NO2_value"] = [-9999999, 9999999]
    tresholds["O3_value"] = [-99999, 9999999]

    for i in range_filters:
        print(i.entity)
        tresholds[i.entity] = [i.lower_treshold, i.upper_treshold]


    data = AIRSensorData.objects.filter(
        Q(SO2_value__lt=tresholds["SO2_value"][0]) |
        Q(SO2_value__gt=tresholds["SO2_value"][1]) |
        Q(NO2_value__lt=tresholds["NO2_value"][0]) |
        Q(NO2_value__gt=tresholds["NO2_value"][1]) |
        Q(O3_value__lt=tresholds["O3_value"][0]) |
        Q(O3_value__gt=tresholds["O3_value"][1])
        ).order_by('date_recorded').values('date_recorded', 'SO2_value', 'NO2_value','O3_value','sensor_location', "id")

    res = []
    for record in data:

        obj = {}
        obj["id"] = record["id"]
        obj["sensor_location"] = record["sensor_location"]
        obj["date_recorded"] = record["date_recorded"].strftime("%Y-%m-%dT%H:%M:%S")
        obj["O3_value"] = record["O3_value"]
        obj["SO2_value"] = record["SO2_value"]
        obj["NO2_value"] = record["NO2_value"]
        # print(obj)
        res.append(obj)

    r = {}
    r["data"] = {"total": len(res), "page": 1, "limit": len(res), "data": res}
    return HttpResponse(json.dumps(r), content_type="application/json")


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def send_email_alerts(request):

    send_air_violations_email()
    send_th_violations_email()
    return HttpResponse(json.dumps([]), content_type="application/json")






def send_th_violations_email():
    range_filters = SensoryDataRangeAlert.objects.all()
    if (len(range_filters) == 0):
        return HttpResponse(json.dumps([]), content_type="application/json")

    tresholds = {}
    tresholds["temperature_value"] = [-9999, 99999]
    tresholds["humidity_value"] = [-9999999, 9999999]
    
    
    for i in range_filters:
        tresholds[i.entity] = [i.lower_treshold, i.upper_treshold]

    data = THSensorData.objects.filter(
        Q(temperature_value__lt=tresholds["temperature_value"][0]) |
        Q(temperature_value__gt=tresholds["temperature_value"][1]) |
        Q(humidity_value__lt=tresholds["humidity_value"][0]) |
        Q(humidity_value__gt=tresholds["humidity_value"][1])).order_by('date_recorded').values('date_recorded', 'temperature_value', 'humidity_value','sensor_location', "id")


    res = []
    for record in data:
        obj = {}
        obj["id"] = record["id"]
        obj["sensor_location"]= record["sensor_location"]
        obj["date_recorded"] = record["date_recorded"].strftime("%Y-%m-%dT%H:%M:%S")
        obj["temperature_value"] = record["temperature_value"]
        obj["humidity_value"] = record["humidity_value"]
        # print(obj)
        res.append(obj)

    # Assuming `res` is defined as shown in the question
    headers = ["ID", "Date Recorded",
               "Temperature", "Humidity","Sensor Location"]
    table = []
    for r in res:
        table.append([r["id"], r["date_recorded"], r["temperature_value"],
                     r["humidity_value"], r["sensor_location"]])

    html = tabulate(table, headers, tablefmt="html")

    email_list = ViolationAlertsList.objects.all()
    recipient_list = []
    for k in email_list:
        recipient_list.append(k.email)

    subject = 'Violation Alerts'
    message = '<h1>Sensory violations</h1>'+html
    from_email = 'example@gmail.com'

    # for additional settings - go to backend/application/settings.py - scroll to bottom
    send_mail(subject=subject, message='', from_email=from_email,
              recipient_list=recipient_list, html_message=message)
    




def send_air_violations_email():
    range_filters = SensoryDataRangeAlert.objects.all()
    if (len(range_filters) == 0):
        return HttpResponse(json.dumps([]), content_type="application/json")

    tresholds = {}
    tresholds["SO2_value"] = [-9999, 99999]
    tresholds["NO2_value"] = [-9999999, 9999999]
    tresholds["O3_value"] = [-99999, 9999999]    
    
    for i in range_filters:
        tresholds[i.entity] = [i.lower_treshold, i.upper_treshold]

    data = AIRSensorData.objects.filter(
        Q(SO2_value__lt=tresholds["SO2_value"][0]) |
        Q(SO2_value__gt=tresholds["SO2_value"][1]) |
        Q(NO2_value__lt=tresholds["NO2_value"][0]) |
        Q(NO2_value__gt=tresholds["NO2_value"][1]) |
        Q(O3_value__lt=tresholds["O3_value"][0]) |
        Q(O3_value__gt=tresholds["O3_value"][1])
        ).order_by('date_recorded').values('date_recorded', 'SO2_value', 'NO2_value','O3_value','sensor_location', "id")


    res = []
    for record in data:
        obj = {}
        obj["id"] = record["id"]
        obj["sensor_location"] = record["sensor_location"]
        obj["date_recorded"] = record["date_recorded"].strftime("%Y-%m-%dT%H:%M:%S")
        obj["O3_value"] = record["O3_value"]
        obj["SO2_value"] = record["SO2_value"]
        obj["NO2_value"] = record["NO2_value"]

        # print(obj)
        res.append(obj)

    # Assuming `res` is defined as shown in the question
    headers = ["ID", "Date Recorded",
               "SO2", "NO2","O3","Sensor Location"]
    table = []
    for r in res:
        table.append([r["id"], r["date_recorded"], r["SO2_value"],
                     r["NO2_value"],r["O3_value"], r["sensor_location"]])

    html = tabulate(table, headers, tablefmt="html")

    email_list = ViolationAlertsList.objects.all()
    recipient_list = []
    for k in email_list:
        recipient_list.append(k.email)

    subject = 'Violation Alerts'
    message = '<h1>Sensory violations</h1>'+html
    from_email = 'example@gmail.com'

    # for additional settings - go to backend/application/settings.py - scroll to bottom
    send_mail(subject=subject, message='', from_email=from_email,
              recipient_list=recipient_list, html_message=message)
    




