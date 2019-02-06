from django.shortcuts import render
from django.utils.safestring import mark_safe
from external_api.models import Device, AirQuality
import datetime
import itertools
from statistics import mean

def index(request):
    devices_data = []
    devices = Device.objects.all()
    delta_24hr = datetime.datetime.now() - datetime.timedelta(days=1)

    for device in devices:
        airquality_log = AirQuality.objects.filter(device_id=device, created_at__gte=delta_24hr).order_by('created_at')

        if airquality_log.count() == 0:
            continue

        grouped_air_log = itertools.groupby(airquality_log, lambda x: x.created_at.strftime("%Y/%m/%d %H:00"))
        grouped_air_log_lst = list(
            map(
                lambda x: (
                    x[0],
                    round(mean(map(lambda y: y.pm25, x[1])), 2)
                ),
                grouped_air_log
            )
        )

        last_update_pm25 = airquality_log.reverse()[0].pm25
        last_update_time = airquality_log.reverse()[0].created_at.strftime('%H:%M')
        warning_str = ''
        color_tag = ''

        if last_update_pm25 < 26:
            warning_str = 'Healthy'
            color_tag = 'good'
        elif last_update_pm25 < 38:
            warning_str = 'Moderate'
            color_tag = 'moderate'
        elif last_update_pm25 < 51:
            warning_str = 'Unhealthy for sensitive'
            color_tag = 'sensitive'
        elif last_update_pm25 < 91:
            warning_str = "Unhealthy"
            color_tag = 'unhealthy'
        else:
            warning_str = "Hazardous"
            color_tag = 'harzardous'

        devices_data.append({
            'name': device.name,
            'slug': device.name.replace(' ', '_').replace('-', '_').replace('.', '_'),
            'location': device.location,
            'air_data': grouped_air_log_lst,
            'label': mark_safe(str(list(map(lambda x: x[0], grouped_air_log_lst)))),
            'value': mark_safe(list(map(lambda x: x[1], grouped_air_log_lst))),
            'last_update_pm25': last_update_pm25,
            'last_update_time': last_update_time,
            'warning': warning_str,
            'color': color_tag,
        })

    data = {"devices": devices_data}

    return render(request, 'report_website/index.html', data)
