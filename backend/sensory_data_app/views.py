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



class ChartConfigSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """
    data_api = serializers.CharField(required = True)
    public_exposed = serializers.BooleanField(required=True)


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
def get_demo_chart_json(request):
    res = '''
    [{
		"id": 1,
		"type": "line",
		"title": " Major change across the week",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"yData": [
			1,
			2,
			3,
			4,
			5,
			6,
			7
		]
	},
	{
		"id": 2,
		"type": "area",
		"title": "Area chart",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"yData": [
			1,
			2,
			3,
			4,
			5,
			6,
			7
		]
	},
	{
		"id": 3,
		"title": "Trends across multiple points",
		"type": "pie",
		"tooltipTitle": "Access from",
		"data": [{
				"value": 1048,
				"name": "Search Engine"
			},
			{
				"value": 735,
				"name": "Direct"
			},
			{
				"value": 580,
				"name": "Email"
			},
			{
				"value": 484,
				"name": "Union Ads"
			},
			{
				"value": 300,
				"name": "Video Ads"
			}
		]
	},
	{
		"id": 4,
		"title": "Trends",
		"type": "stacked-line",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"data": [{
				"name": "Email",
				"type": "line",
				"stack": "Total",
				"data": [
					120,
					132,
					101,
					134,
					90,
					230,
					210
				]
			},
			{
				"name": "Union Ads",
				"type": "line",
				"stack": "Total",
				"data": [
					220,
					182,
					191,
					234,
					290,
					330,
					310
				]
			},
			{
				"name": "Video Ads",
				"type": "line",
				"stack": "Total",
				"data": [
					150,
					232,
					201,
					154,
					190,
					330,
					410
				]
			},
			{
				"name": "Direct",
				"type": "line",
				"stack": "Total",
				"data": [
					320,
					332,
					301,
					334,
					390,
					330,
					320
				]
			},
			{
				"name": "Search Engine",
				"type": "line",
				"stack": "Total",
				"data": [
					820,
					932,
					901,
					934,
					1290,
					1330,
					1320
				]
			}
		]
	},
	{
		"id": 5,
		"title": "Bar chart",
		"type": "bar",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"yData": [
			120,
			200,
			150,
			80,
			70,
			110,
			130
		]
	}
]    '''
    
    res = '''
    {
		"id": 1,
		"type": "line",
		"title": " Major change across the week",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"yData": [
			1,
			2,
			3,
			4,
			5,
			6,
			7
		]
	}'''
    return HttpResponse(res, content_type="application/json")


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_demo_chart_json_two(request):
    res = '''
    {
		"id": 2,
		"type": "area",
		"title": "Area chart",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"yData": [
			1,
			2,
			3,
			4,
			5,
			6,
			7
		]
	}'''
    return HttpResponse(res, content_type="application/json")



@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_demo_chart_json_three(request):
    res = '''
    {
		"id": 3,
		"title": "Trends across multiple points",
		"type": "pie",
		"tooltipTitle": "Access from",
		"data": [{
				"value": 1048,
				"name": "Search Engine"
			},
			{
				"value": 735,
				"name": "Direct"
			},
			{
				"value": 580,
				"name": "Email"
			},
			{
				"value": 484,
				"name": "Union Ads"
			},
			{
				"value": 300,
				"name": "Video Ads"
			}
		]
	}'''
    return HttpResponse(res, content_type="application/json")


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_demo_chart_json_four(request):
    res = '''
    
	{
		"id": 4,
		"title": "Trends",
		"type": "stacked-line",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"data": [{
				"name": "Email",
				"type": "line",
				"stack": "Total",
				"data": [
					120,
					132,
					101,
					134,
					90,
					230,
					210
				]
			},
			{
				"name": "Union Ads",
				"type": "line",
				"stack": "Total",
				"data": [
					220,
					182,
					191,
					234,
					290,
					330,
					310
				]
			},
			{
				"name": "Video Ads",
				"type": "line",
				"stack": "Total",
				"data": [
					150,
					232,
					201,
					154,
					190,
					330,
					410
				]
			},
			{
				"name": "Direct",
				"type": "line",
				"stack": "Total",
				"data": [
					320,
					332,
					301,
					334,
					390,
					330,
					320
				]
			},
			{
				"name": "Search Engine",
				"type": "line",
				"stack": "Total",
				"data": [
					820,
					932,
					901,
					934,
					1290,
					1330,
					1320
				]
			}
		]
	}'''
    return HttpResponse(res, content_type="application/json")


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_demo_chart_json_five(request):
    res = '''
    {
		"id": 5,
		"title": "Bar chart",
		"type": "bar",
		"xData": [
			"Mon",
			"Tue",
			"Wed",
			"Thu",
			"Fri",
			"Sat",
			"Sun"
		],
		"yData": [
			120,
			200,
			150,
			80,
			70,
			110,
			130
		]
	}
'''
    return HttpResponse(res, content_type="application/json")
