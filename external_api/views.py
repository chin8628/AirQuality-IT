from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import AirQuality, Device
from django.views.decorators.http import require_POST

@require_POST
def add(request):
    token = request.POST.get('token')
    device_id = request.POST.get('id')

    try:
        Device.objects.get(device_id=device_id, token=token)
    except ObjectDoesNotExist:
        return HttpResponse('Failed: Token or Device ID not found')

    pm10 = request.POST.get('pm10', 0)
    pm25 = request.POST.get('pm25', 0)
    pm1 = request.POST.get('pm1', 0)

    device = Device.objects.get(device_id=device_id)
    AirQuality(device_id=device, pm1=pm1, pm10=pm10, pm25=pm25).save()

    return HttpResponse("Done")
