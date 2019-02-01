from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import AirQuality, Device

def add(request):
    token = request.GET.get('token')
    device_id = request.GET.get('id')

    try:
        Device.objects.get(device_id=device_id, token=token)
    except ObjectDoesNotExist:
        return HttpResponse('Failed: Token or Device ID not found')

    pm25, pm10 = request.GET.get('pm25'), request.GET.get('pm10')

    device = Device.objects.get(device_id=device_id)
    AirQuality(device_id=device, pm10=pm10, pm25=pm25).save()

    return HttpResponse("Done")
