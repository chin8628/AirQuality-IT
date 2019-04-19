from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.db.models import Avg
from django.db.models.functions import Trunc

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AirQuality, Device
from .serializers import AirQualitySerializer, DeviceSerializer, AverageAirQualitySerializer


@require_POST
def add(request):
    token = request.POST.get('token', 0)
    device_id = request.POST.get('id', 0)

    try:
        Device.objects.get(device_id=device_id, token=token)
    except ObjectDoesNotExist:
        return HttpResponse('Failed: Token or Device ID not found')

    pm100 = request.POST.get('pm100', 0)
    pm25 = request.POST.get('pm25', 0)
    pm10 = request.POST.get('pm10', 0)

    device = Device.objects.get(device_id=device_id)
    AirQuality(device_id=device, pm10=pm10, pm100=pm100, pm25=pm25).save()

    return HttpResponse("Done")


@api_view(['GET'])
def devices(request):
    devices = Device.objects.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def airquality_logs(request, device_id, hours):
    hours = 24 if hours > 24 else hours
    hours = 1 if hours < 1 else hours

    time_delta = datetime.now() - timedelta(hours=hours)

    airquality = AirQuality.objects.filter(created_at__gte=time_delta, device_id=device_id).annotate(created_at_trunced_hour=Trunc(
        'created_at', 'hour')).values('created_at_trunced_hour').annotate(avg_pm25=Avg('pm25'), avg_pm100=Avg('pm100'), avg_pm10=Avg('pm10'))

    serializer = AverageAirQualitySerializer(airquality, many=True, context={'request': request})

    return Response(serializer.data)


@api_view(['GET'])
def lastest_aqi_log(request, device_id):
    last_record = AirQuality.objects.filter(device_id=device_id).last()
    serializer = AirQualitySerializer(last_record, context={'request': request})

    return Response(serializer.data)


@api_view(["GET"])
def get_device(request, device_id):
    device = Device.objects.get(device_id=device_id)
    serializer = DeviceSerializer(device)
    return Response(serializer.data)
